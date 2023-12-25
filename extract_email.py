from bs4 import BeautifulSoup
from selenium import webdriver

from extract_emails.utils import email_filter

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

#function that extracts all emails from a page you provided and stores them in a list
def emailExtractor(urlString):
    
    emailList = []
    filtered_emails = []

    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(10)
        driver.get(urlString)
        
        h=driver.page_source
        soup=BeautifulSoup(h,'html.parser')
        mailtos = soup.select('a[href]')
        
        for i in mailtos:
            href=i['href']
            
            if "mailto" in href:
                email_text = i['href'].replace("mailto:", "")
                email_text = email_text.split("?").pop(0)
                email_text = email_text.strip()

                if email_text:
                    emailList.append(email_text)

        filtered_emails = email_filter(emailList)
    except:
        pass

    return ", ".join(filtered_emails)
