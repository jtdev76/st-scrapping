import pandas as pd
import sys
sys.path.append('./')
from extract_email import emailExtractor

df = pd.read_excel("./clutch.xlsx")

def test(row):
    try:
        row["Email"] = emailExtractor(row["Website"])
    except:
        row["Email"] = ""
    print(row["Website"], row["Email"])

df.apply(lambda x: test(x), axis=1)
df = df[df["Email"] != ""]

df.to_excel("./clutch_filtered.xlsx", index = False)
