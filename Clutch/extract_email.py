from bs4 import BeautifulSoup
import requests


#function that extracts all emails from a page you provided and stores them in a list
def emailExtractor(urlString):
    emailList = set()

    getH=requests.get(urlString, timeout=10)
    h=getH.content
    soup=BeautifulSoup(h,'html.parser')
    mailtos = soup.select('a[href]')
    
    for i in mailtos:
        href=i['href']
        
        if "mailto" in href:
            emailList.add(i.text)

    return ", ".join(emailList)

# print(emailExtractor("http://www.amconsoft.com/"))