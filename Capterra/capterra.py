# import requests
import json
import pandas as pd
import sys
sys.path.append('..')
import check_scrapped_records
import time
from requests.exceptions import RequestException, JSONDecodeError
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import extract_email
directory = "RAW_data"
data_list = []  # List to store extracted data

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)

        with open(filepath, 'r') as file:
            json_data = json.load(file)

            for data in json_data:
                context = {}
                context['name'] = data.get('node').get('name')
                context['websiteUrl'] = data.get('node').get('websiteUrl')
                context['city'] = data.get('node').get('physicalLocations')[0].get('city') if data.get('node').get('physicalLocations') else None
                context['state'] = data.get('node').get('physicalLocations')[0].get('state') if data.get('node').get('physicalLocations') else None
                context['countryCode'] = data.get('node').get('physicalLocations')[0].get('countryCode') if data.get('node').get('physicalLocations') else None

                if check_scrapped_records.check_records(context['name']):
                    context['email'] = extract_email.emailExtractor(data.get('node').get('websiteUrl'))
                    if context['email']:
                        print(context['email'])
                        data_list.append(context)


check_scrapped_records.save_records()
df = pd.DataFrame(data_list)
df.to_excel("Capterra.xlsx", index=False)
