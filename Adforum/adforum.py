from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

data_list = []
link_list = []
base_url = "https://www.adforum.com"
headers = {'X-Requested-With': 'XMLHttpRequest'}
# pagination = requests.get("https://www.adforum.com/directories/agency/digital?location=country:United%20States&discipline_strkey=DSP133")
# paginate_res = BeautifulSoup(pagination.text, 'html.parser')
# print(paginate_res.find('button',{"id": "btnLoadmore"}))
pagination = requests.get("https://www.adforum.com/search/find/loadmore?location=country:United%20States&discipline_strkey=DSP133&e=agency&rtpl=ListEntities&l=8&o=&p=1",headers=headers)
paginate_res  = json.loads(pagination.text)
total_count = paginate_res.get('cnt')
page = 1
while total_count != len(link_list): 
  response = requests.get(f"https://www.adforum.com/search/find/loadmore?location=country:United%20States&discipline_strkey=DSP133&e=agency&rtpl=ListEntities&l=8&o=&p={page}",headers=headers)
  json_obj  = json.loads(response.text)
  soup = BeautifulSoup(json_obj['html'], 'html.parser')
  for url in soup.find_all(class_="b-search_result__link--title"):
    link_list.append(base_url+url.get('href'))
  page += 1

  if page == 2:
    break
  print("page==",page)
  print("links==",len(link_list))
for url in link_list:
  details = {}
  driver = webdriver.Chrome()
  driver.get(url)
  details['Company'] =driver.find_element(By.CLASS_NAME,"af-company-title").text
  for item in driver.find_elements(By.CLASS_NAME,"agency-info__text--alt"):
    span = item.find_elements(By.TAG_NAME,"span")
    # print("span0000==",span)
    key =span[0].text
    if key =="PHONE:":
      details["Phone"] = span[1].text
    if key == "EMAIL:":
      details['Email']=item.find_element(By.TAG_NAME,"a").text
    if key == 'WEBSITE:':
      details['Website']=item.find_element(By.TAG_NAME,'a').get_attribute("href")
    details['Address'] = driver.find_element(By.TAG_NAME,'address').text
  print(details)
  data_list.append(details)
df = pd.DataFrame(data_list)
df.to_excel('data.xlsx', index=False)  # Set index=False to exclude row numbers
print("Excel file created successfully.")

  # res = requests.get(url)
  # soup = BeautifulSoup(res.text,"html.parser")
  # details['Company'] = soup.find(class_="af-company-title").get_text(strip=True)
  # if soup.find('address').get_text(strip=True):
  #   details['Address'] = soup.find('address').get_text(strip=True)
  # for item in soup.find_all(class_="agency-info__text--alt"):
  #   key = item.find("span").get_text(strip=True)
  #   print(key =="Phone:")
  #   if key =="Phone":
  #     print("phone")
  #   if key == "Email:":
  #     print(item.find('a'),"11111111111111")