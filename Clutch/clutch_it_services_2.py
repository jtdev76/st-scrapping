import sys
sys.path.append('..')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import check_scrapped_records

import pandas as pd

old_records = pd.read_excel("clutch_it_services_2.xlsx")

def fetch_website_url(row):

    if str(row["Website"]) == "nan":
        if check_scrapped_records.check_records(row["Name"]):
            driver = webdriver.Chrome()
            driver.get(row["Clutch url"])

            try:
                web_link_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".visit-website"))
                )
                row["Website"] = web_link_element.get_attribute("href")
            except:
                pass

    return row

new_records = old_records.apply(lambda x: fetch_website_url(x), axis=1)

new_records.to_excel("./clutch_it_services_2.xlsx", index = False)