from bs4 import BeautifulSoup
import requests


#add url of the page you want to scrape to urlString
urlString='https://ctccarriers.com/'
def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16)^k)

    return de

#function that extracts all emails from a page you provided and stores them in a list
def emailExtractor(urlString):
    emailList = set()

    getH=requests.get(urlString)
    h=getH.content
    soup=BeautifulSoup(h,'html.parser')
    mailtos = soup.select('a[href]')
    
    for i in mailtos:
        href=i['href']
        
        if "mailto" in href:
            emailList.add(i.text)

    return ", ".join(emailList)

# print(emailExtractor(urlString))