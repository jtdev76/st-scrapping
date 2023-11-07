from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument('--headless')

from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time

from extract_email import emailExtractor
# import check_scrapped_records

data_list = []

counter = 1
for page in range(91):
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("https://clutch.co/logistics/supply-chain-management?page={page}".format(page=str(page)))

        cluch_links = driver.find_elements(By.CSS_SELECTOR, ".website-profile")
    
        for cluch_link in cluch_links:
            try:
                row_data = {
                    "Name": "",
                    "Email": "",
                    "Clutch url": cluch_link.find_element(By.CSS_SELECTOR, "a").get_attribute("href"),
                    "Website": "",
                }
                
                page_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                page_driver.get(row_data["Clutch url"])

            
                web_link_element = WebDriverWait(page_driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".visit-website"))
                )

                web_link = web_link_element.get_attribute("href")

                profile_header = WebDriverWait(page_driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".profile-header__title"))
                )

                row_data["Name"] = profile_header.text
                row_data["Email"] = emailExtractor(web_link)
                row_data["Website"] = web_link

                # if check_scrapped_records.check_records(row_data["Name"]):
                data_list.append(row_data)
                df = pd.DataFrame(data_list)
                df.to_excel("./clutch.xlsx", index = False)

                    # check_scrapped_records.save_records()

                print(counter)
                counter += 1
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)