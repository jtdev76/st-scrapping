import requests
import json
import sys
# from extract_email import emailExtractor
sys.path.append('..')
import check_scrapped_records
import extract_email
import pandas as pd

data_list = []

total_page = 22
counter =1
for page in range(total_page): #{str(page_no)}
    print(page)
    page_no = page+1
    page = f"page-{page+1}.json"
    response = requests.get(f"https://www.semrush.com/agencies/_next/data/agency-directory/en/category/ssg/united-states/page-{str(page_no)}.json")
    # json_data = json.dumps(response.text)
    data = json.loads(response.text)

    agencyList = data['pageProps']['initialReduxState']["list"]["data"]['agencyList']

    for agencyList in agencyList:
        alias_name = agencyList['alias']
        # print(alias_name)
        
        company_data = requests.get(f"https://www.semrush.com/agencies/_next/data/agency-directory/en/{alias_name}.json", timeout=300)
        json_data_company = json.loads(company_data.text)
        agency_info = json_data_company['pageProps']['initialReduxState']['agencyPage']['data']['agencyInfo']
        context = {}

        website = agency_info['offices'][0]['website']
        print(website)
        if website.startswith("https://"):
            website = website
        else:
            website = 'https://'+website
        email = extract_email.emailExtractor(website)
        # print(email)
        if len(email)>0:
            context["Company"] = agency_info['name']
            context['Email'] = email
            # context[agency_info['offices'][0]['location']['type']] = agency_info['offices'][0]['location']['name']
            context['Website'] = website
            context['Address'] = agency_info['offices'][0]['address']

            # print(context, '------------------------#################################--------------------------------------------')
            counter += 1
            print(counter, email)

            company_found = check_scrapped_records.check_records(context["Company"])

            if company_found :
                data_list.append(context)

    
# https://www.octivdigital.com


df = pd.DataFrame(data_list)

df.to_excel("semrush.xlsx", index = False)

check_scrapped_records.save_records()