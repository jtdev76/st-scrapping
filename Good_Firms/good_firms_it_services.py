import sys
sys.path.append('..')

from bs4 import BeautifulSoup
import requests
import pandas as pd

import extract_email
import check_scrapped_records

data_list = []



counter = 0

for i in range(1, 74):
    next_url = "https://www.goodfirms.co/it-services/usa?page="+str(i)
    
    response = requests.get(next_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for row in soup.select(".firm-wrapper"):
        try:
            row_data = {
                "Name": row["entity-name"],
                "Email": "",
                "Location": row.select_one(".firm-location").text,
                "Website": row.select_one(".web-url")["href"],
            }
            print(row_data["Website"])

            if check_scrapped_records.check_records(row_data["Name"]):
                row_data["Location"] = row_data["Location"].strip()

                row_data["Email"] = extract_email.emailExtractor(row_data["Website"])

                if not row_data["Email"]:
                    continue

                data_list.append(row_data)

                counter+=1
                print(counter, row_data["Email"])
            else:
                print("Already Available: ", row_data["Name"])
        except:
            pass


check_scrapped_records.save_records()

df = pd.DataFrame(data_list)

df.to_excel("Good Firms IT services.xlsx", index = False)