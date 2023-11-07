from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time

data_list = []

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def start_scrape():
    response = requests.get("https://admin-ecohub.herokuapp.com/get-spots?organizationFields=&businessFields=renewable+energy&hotSpotFields=&greenSpotFields=&countries=USA&filterType=business")
    data = response.json()

    i = 0
    for row in data["spots"]:
        scrape_individual_pages(row)
        print(i)
        i+=1

def scrape_individual_pages(row):
    print("row", row)
    url = "https://www.ecohubmap.com/company/business/test/"+row["key"]
    driver.get(url)

    row_data = {
        "Name": row["name"],
        "Email": "",
        "Country": row["country"],
        "Address": "",
        "Ecohubmap url": url,
        "Website url": "",
        "About": "",
    }

    main_elements = driver.find_elements(By.CSS_SELECTOR, ".CompaniesContainer_infoCard__HpGAO")
    for main_element in main_elements:
        element_type = main_element.find_element(By.CSS_SELECTOR, '.CompaniesContainer_infoText__waQaD').text
        element_text = main_element.find_element(By.CSS_SELECTOR, '.CompaniesContainer_infoUrl__Sd6Lg').text

        if(element_type == "WEBSITE"):
            row_data["Website url"] = element_text
        elif(element_type == "EMAIL"):
            row_data["Email"] = element_text
        elif(element_type == "LOCATION"):
            row_data["Address"] = element_text

    try:
        about_div = driver.find_element(By.CSS_SELECTOR, ".CompaniesContainer_currentSpotInfoDesc__Nyreq")
        
        if about_div:
            row_data["About"] = about_div.text
    except:
        pass

    data_list.append(row_data)

if __name__ == '__main__':
    start_scrape()

    df = pd.DataFrame(data_list)

    df.to_excel("data/ecohubmap.xlsx", index = False)