from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
sys.path.append('..')

options = Options()
# options.add_argument('--headless')

options2 = Options()
# options2.add_argument('--headless')

from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time

import extract_email
import check_scrapped_records

data_list = []

counter = 1

for page in range(199):

    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://clutch.co/us/it-services?sort_by=Verification&page={page}".format(page=str(page)))

        cluch_links = driver.find_elements(By.CSS_SELECTOR, ".provider-row")
    
        for cluch_link in cluch_links:
            
            website_url = ""
            try:
                website_obj = cluch_link.find_element(By.CSS_SELECTOR, ".website-link__item")
                if website_obj:
                    website_url = website_obj.get_attribute("href")
            except:
                pass

            try:
                row_data = {
                    "Name": cluch_link.find_element(By.CSS_SELECTOR, ".company_info").text,
                    "Email": "",
                    "Clutch url": cluch_link.find_element(By.CSS_SELECTOR, ".website-profile a").get_attribute("href"),
                    "Website": website_url,
                }

                data_list.append(row_data)
                print(row_data)

                continue
                
                page_driver = webdriver.Chrome(options=options2)
                page_driver.get(row_data["Clutch url"])

                web_link_element = WebDriverWait(page_driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".visit-website"))
                )

                web_link = web_link_element.get_attribute("href")

                profile_header = WebDriverWait(page_driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".profile-header__title"))
                )

                row_data["Name"] = profile_header.text

                # if check_scrapped_records.check_records(row_data["Name"]):
                row_data["Email"] = extract_email.emailExtractor(web_link)
                print(counter, profile_header.text, row_data["Email"])

                if row_data["Email"]:
                    row_data["Website"] = web_link

                    data_list.append(row_data)
                    df = pd.DataFrame(data_list)
                    df.to_excel("./clutch_it_services.xlsx", index = False)


                counter += 1
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


# check_scrapped_records.save_records()
        
df = pd.DataFrame(data_list)
df.to_excel("./clutch_it_services.xlsx", index = False)