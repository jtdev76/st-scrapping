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
    page = 1

    while True:
        payload = {
            'search_categories[]': '55',
            'per_page': '25',
            'page': page
        }
        response = requests.post("https://www.insertbiz.com/jm-ajax/get_listings/", data=payload)
        data = response.json()

        
        for row in data['listings']:
            try:
                scrape_individual_pages(row)
            except:
                pass

        if data['max_num_pages'] > page:
            page += 1
        else:
            break


def scrape_individual_pages(row):
    driver.get(row['permalink'])

    row_data = {
        "Title": row["title"],
        "Email": "",
        "Country": "",
        "Telephone": row["telephone"],
        "Address": row["location"]['raw'] + ", " + row["location"]['address'],
        "Insertbiz_url": row['permalink'],
        "Website url": row["json_ld"]["mainEntityOfPage"]["@id"],
        "Content": row["json_ld"]["description"],
    }

    try:
        email_div = driver.find_element(By.CSS_SELECTOR, ".listing-email")
        
        if email_div:
            row_data["Email"] = email_div.text
    except:
        pass

    try:
        country_div = driver.find_element(By.CSS_SELECTOR, ".job_listing-location-formatted")
        
        if country_div:
            row_data["Country"] = country_div.text
    except:
        pass

    data_list.append(row_data)

if __name__ == '__main__':
    try:
        start_scrape()
    except:
        pass

    df = pd.DataFrame(data_list)

    df.to_excel("data/insertbiz.xlsx", index = False)