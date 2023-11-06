from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time

data_list = []

counter = 0

response = requests.get("https://www.altenergymag.com/company_directory_search.php?company=&industry=&region=&sector=&keyword=&Search=active&search=Search#results")

soup = BeautifulSoup(response.content, 'html.parser')

for row in soup.select(".entry-title"):

    try:
        url = row.select_one("a")['href']
        title = row.select_one("a").text

        row_data = {
            "Title": title,
            "Company Category": "",
            "Email": "",
            "Telephone": "",
            "Address": "",
            "Website": "",
            "Description": ""
        }

        try:
            response_indivisual = requests.get("https://www.altenergymag.com"+url)
            soup_indivisual = BeautifulSoup(response_indivisual.content, 'html.parser')

            page = soup_indivisual.select_one(".page-content")

            try:
                row_data['Description'] = page.select_one(".description").text
                row_data['Description'] = row_data['Description'].strip()
            except:
                pass

            try:
                mailtos = soup_indivisual.select('a[href]')
        
                for i in mailtos:
                    href=i['href']
                    
                    if "mailto" in href:
                        row_data['Email'] = href.replace("mailto:", "")
            except:
                pass


            try:
                ps = soup_indivisual.select('p')
        
                for p in ps:
                    
                    try:
                        if "Mailing Address:" in p.text:
                            row_data['Address'] = p.text
                            row_data['Address'] = row_data['Address'].replace("Mailing Address:", "")
                            row_data['Address'] = row_data['Address'].strip()
                    except:
                        pass
                    
                    try:
                        if "Website:" in p.text:
                            row_data['Website'] = p.text
                            row_data['Website'] = row_data['Website'].replace("Website:", "")
                            row_data['Website'] = row_data['Website'].strip()
                    except:
                        pass

                    try:
                        if "Tel:" in p.text:
                            row_data['Telephone'] = p.text
                            row_data['Telephone'] = row_data['Telephone'].replace("Tel:", "")
                            row_data['Telephone'] = row_data['Telephone'].strip()
                    except:
                        pass

                    try:
                        if "Company Category:" in p.text:
                            row_data['Company Category'] = p.text
                            row_data['Company Category'] = row_data['Company Category'].replace("Company Category:", "")
                            row_data['Company Category'] = row_data['Company Category'].strip()
                    except:
                        pass
            except:
                pass

        except Exception as e:
            print(e)


        data_list.append(row_data)

        counter+=1
        print(counter)

    except Exception as e:
        print(e)

df = pd.DataFrame(data_list)

df.to_excel("data/altenergymag.xlsx", index = False)