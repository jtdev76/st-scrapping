import sys
sys.path.append('..')

import check_scrapped_records
from extract_email_without_selenium import emailExtractor
import pandas as pd

old_records = pd.read_excel("clutch_it_services_2.xlsx")

def fetch_website_url(row):

    if str(row["Website"]) != "nan":
        if check_scrapped_records.check_records(row["Name"]):
            row["Email"] = emailExtractor(row["Website"])
            print(row["Email"])
        else:
            row["Email"] = ""
    else:
        row["Email"] = ""
        
    return row

new_records = old_records.apply(lambda x: fetch_website_url(x), axis=1)

new_records = new_records[new_records["Email"] != ""]

new_records.to_excel("./clutch_it_services_4.xlsx", index = False)