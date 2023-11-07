from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
sys.path.append('..')
import check_scrapped_records
data_list = []
url = "https://soravjain.com/digital-marketing-agencies-india/"
counter = 1
payload = {}
headers = {}
response = requests.request("GET", url, headers={}, data={})
soup = BeautifulSoup(response.text, 'html.parser')
h3_tags = soup.find_all('h3',class_="wp-block-heading")
h3_tags.pop()
for h3_tag in h3_tags:
    company = {}
    companyName = h3_tag.get_text(strip=True).split('. ')
    if len(companyName)>1:
      company_found = check_scrapped_records.check_records(companyName[1])
      company['Company Name'] = companyName[1] if company_found else companyName[0]
    else:
      print(companyName)
    next_element = h3_tag.find_next_sibling()
    while next_element and next_element.name != 'h3' and company_found:
      if next_element.name == 'p':
        text = next_element.get_text()
        if 'Address –' in text:
          company["Address"] = text[len("Address –"):].strip()
        if 'Email –' in text:
          company["Email"] = text[len("Email –"):].strip()
        if 'Phone No –' in text:
          company["Phone"] = text[len("Phone No –"):].strip()
        if "Website –" in text:
          company["Website"] = text[len("Website –"):].strip()
        # if "Brands –" in text:
        #   company['Brands'] = text[len("Brands –"):].strip()
        # if "Services –" in text:
        #   company["Services"] = text[len("Services –"):].strip()
      next_element = next_element.find_next_sibling()
    if company_found:
      data_list.append(company)
    else:print(company,"-----",counter,h3_tag)
    counter += 1
check_scrapped_records.save_records()
df = pd.DataFrame(data_list)
df.to_excel("souravjain.xlsx", index = False)
