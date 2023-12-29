import sys
sys.path.append('..')

import check_scrapped_records
import pandas as pd

old_records = pd.read_excel("clutch_it_services_4.xlsx")

def fetch_website_url(row):

    if check_scrapped_records.check_records(row["Name"]):
        pass
        
    return row

old_records.apply(lambda x: fetch_website_url(x), axis=1)

check_scrapped_records.save_records()