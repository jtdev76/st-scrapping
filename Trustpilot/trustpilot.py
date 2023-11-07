import requests
import json
import pandas as pd
import sys
sys.path.append('..')
import check_scrapped_records

data_list = []

url1 =  "https://www.trustpilot.com/_next/data/categoriespages-consumersite-3760/categories/energy_power.json?categoryId=energy_power"
response1 = requests.request("GET", url1, headers={}, data={})
json_obj = json.loads(response1.text)
total = json_obj.get("pageProps")['businessUnits']["totalPages"]

for page in range(1,total+1):
  if page != 1:
    url = f"https://www.trustpilot.com/_next/data/categoriespages-consumersite-3760/categories/energy_power.json?page={str(page)}&categoryId=energy_power"
  else:
    url = "https://www.trustpilot.com/_next/data/categoriespages-consumersite-3760/categories/energy_power.json?categoryId=energy_power"
  print("------",page,"------------")
  response = requests.request("GET", url, headers={}, data={})
  json_obj = json.loads(response.text)
  for data in json_obj.get("pageProps")['businessUnits']['businesses']:
    row_data = {}
    row_data["Company"] = data['displayName']
    if data["contact"]:
      row_data["Email"] = data["contact"]["email"] if data["contact"]["email"] else ""
      row_data["Phone"] = data["contact"]["phone"] if data["contact"]["phone"] else ""
      row_data["Website"] = data["contact"]["website"] if data["contact"]["website"] else ""
    if data["location"]:
      address =[]
      for value in data["location"].values():
        if value:
          address.append(value)
      row_data["Address"]= ", ".join(address)
    company_found = check_scrapped_records.check_records(row_data["Company"])
    if company_found:
      data_list.append(row_data)
    check_scrapped_records.save_records()

df = pd.DataFrame(data_list)
df.to_excel('trustpilot.xlsx', index=False)  # Set index=False to exclude row numbers
