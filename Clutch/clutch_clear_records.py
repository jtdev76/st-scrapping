import pandas as pd
import sys
sys.path.append('./')
import check_scrapped_records

df = pd.read_excel("./clutch.xlsx")

def test(row):
    if str(row["Email"]) == "nan":
        row["Email"] = ""
    
    row["Email"] = str(row["Email"]).strip()

    company_found = check_scrapped_records.check_records(row["Name"])
    if not company_found:
        row["Email"] = ""

df.apply(lambda x: test(x), axis=1)
df = df[df["Email"] != ""]

df.to_excel("./clutch_filtered.xlsx", index = False)

check_scrapped_records.save_records()