from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time

data_list = []

counter = 0

response = requests.get("https://www.keyfactsenergy.com/directory/list/?country_id=146")

soup = BeautifulSoup(response.content, 'html.parser')

for row in soup.select(".article-small"):

    try:
        url = row.select_one(".article__title a")['href']
        title = row.select_one(".article__title a").text
        shot_description = row.select_one(".article__entry").text
        shot_description = shot_description.strip()
        
        email = ""

        try:
            response_indivisual = requests.get("https://www.keyfactsenergy.com"+url)
            soup_indivisual = BeautifulSoup(response_indivisual.content, 'html.parser')

            mailtos = soup_indivisual.select('.article__entry a[href]')
    
            for i in mailtos:
                href=i['href']
                
                if "mailto" in href:
                    email = href.replace("mailto:", "")

            print("email", email)
        except Exception as e:
            print(e)

        try:
            row_data = {
                "Title": title,
                "Email": email,
                "Shot Description": shot_description
            }

            data_list.append(row_data)
        except Exception as e:
            print(e)

        counter+=1
        print(counter)

    except Exception as e:
        print(e)

df = pd.DataFrame(data_list)

df.to_excel("data/keyfactsenergy.xlsx", index = False)