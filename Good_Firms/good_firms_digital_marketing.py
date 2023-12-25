from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import sys
sys.path.append('..')
import check_scrapped_records
import extract_email

data_list = []
counter = 0

# Path to your WebDriver executable. Download the WebDriver for your browser.
driver_path = '/path/to/your/driver/executable'

# Set up the WebDriver (in this case, Chrome)
driver = webdriver.Chrome()

for i in range(1, 8):
    next_url = "https://www.goodfirms.co/directory/marketing-services/top-digital-marketing-companies?locations%5B167%5D=us&services%5B11%5D=14&page="+str(i)
    driver.get(next_url)

    # Waiting for the page to load (adjust as needed)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(10)
    for row in soup.select(".firm-wrapper"):
        try:
            row_data = {
                "Name": row["entity-name"],
                "Email": "",
                "Location": row.select_one(".firm-location").text,
                "Website": row.select_one(".web-url")["href"],
            }

            data1 = row.select_one(".firm-short-description").select_one(".profile-link")["href"]
            driver.get(data1)
            time.sleep(10)

            soup1 = BeautifulSoup(driver.page_source, 'html.parser')
            for names in soup1.find("div", {"class":"entity-service-focus-slider"}).find("div", {"class": "carousel-inner"}).find_all("div", {"class": "item carousel-item active"}):
                time.sleep(2)
                if names.find("div", {"class":'entity-focus-slider-legend'}).text.strip() == "Digital Marketing":

                    marketing_percentage = names.find("div",{"class":'entity-focus-slider-percentage'}).text.strip()
                    row_data["marketing_percentage"] = float(marketing_percentage.strip("%"))/100
                    print(row_data["marketing_percentage"])
                    # print(int(names.find("div",{"class":'entity-focus-slider-percentage'}).text.strip())) # type str
                else:
                    pass
                break
            
            if check_scrapped_records.check_records(row_data["Name"]):
                row_data["Location"] = row_data["Location"].strip()

                row_data["Email"] = extract_email.emailExtractor(row_data["Website"])
                # numeric_values = [float(pct.strip('%')) / 100.0 for pct in row_data["marketing_percentage"]]
                
                if row_data["marketing_percentage"] >= 0.5 and row_data["Email"]:
                    data_list.append(row_data)
                counter += 1
                print(counter, row_data["Email"])
            else:
                print("Already Available: ", row_data["Name"])

        except Exception as e:
            pass

# Close the browser
driver.quit()

# Save data to Excel
df = pd.DataFrame(data_list)
df.to_excel("Good Firms Digital Marketing.xlsx", index=False)
