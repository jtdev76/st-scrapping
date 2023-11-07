from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time

data_list = []

i = 0
page = 1

while True:
    response = requests.get("https://solarchronicle.in/business-directory/page/"+str(page))
    page += 1

    soup = BeautifulSoup(response.content, 'html.parser')

    if not soup.find_all(class_="wpbdp-listing"):
        break

    for row in soup.find_all(class_="wpbdp-listing"):
        
        try:
            address = row.find(class_="address-info").get_text(separator=', ')
            address = address.replace("Address:", "")
            address = address.replace("\n",", ")
            address = address.replace(" ,",",")
            address = address.replace(",,",",")
            address = address.replace(",,",",")
            address = address.strip()
            address = address.strip(",")
            address = address.strip()
        except:
            address = ""
        
        try:
            category = row.find(class_="wpbdp-field-association-category").text
            category = category.replace("Category:", "")
            category = category.strip()
        except:
            category = ""

        try:
            company_email = row.select_one(".wpbdp-field-company_email .value").text
        except:
            company_email = ""

        try:
            business_phone = row.select_one(".wpbdp-field-business_phone .value").text
        except:
            business_phone = ""

        try:
            website = row.select_one(".wpbdp-field-website a")['href']
        except:
            website = ""

        try:
            row_data = {
                "Title": row.find(class_="listing-title").text.strip(),
                "Company Email": company_email,
                "Address": address,
                "Category": category,
                "Business Phone": business_phone,
                "Website": website
            }

            data_list.append(row_data)
        except:
            pass

        i+=1
        print(i)

df = pd.DataFrame(data_list)

df.to_excel("data/solarchronicle.xlsx", index = False)