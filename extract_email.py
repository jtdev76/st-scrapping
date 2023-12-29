from bs4 import BeautifulSoup
import requests

from extract_emails.utils import email_filter

#function that extracts all emails from a page you provided and stores them in a list
def emailExtractor(urlString):
    
    emailList = []
    filtered_emails = []

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        req = requests.get(urlString, headers=headers, timeout=10)
        h = req.content
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
