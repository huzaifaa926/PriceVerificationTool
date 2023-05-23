from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
from decimal import Decimal

LIMIT = 10
options = Options()
options.add_argument("--headless")

def normalize_url(url):
    if url.startswith('//'):
        url = url[2:]
    return url.lstrip('/')


def scrap(keyword):
    keyword = urllib.parse.quote(keyword)
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={keyword}&viewtype=G&page=1")
    html = driver.page_source
    driver.close()

    soup = BeautifulSoup(html, 'lxml')
    product_lists = soup.find('div', {'class': 'app-organic-search__list'}).findChildren("div" , recursive=False)
    data = []
    for product in product_lists[:LIMIT]:
        temp = {}
        if product.find('h2'):
            link = product.find('h2').find('a')['href']
            link = 'https://' + normalize_url(link)
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
            response=requests.get(link, headers=headers)
            soup=BeautifulSoup(response.text,'lxml')
            title = soup.find('div', {'class':'product-title'})
            price = soup.find('div', {'class':'product-price'}).find_all(class_='price')
            quality = soup.find('div', {'class':'product-price'}).find_all(class_='quality')
            UoM = soup.find('div', {'class':'product-price'}).find_all(class_='unit')

            if title:
                title = title.text.strip()
            if price:
                price = price[0].text.strip()
                match = re.search(r'\d+(?:,\d+)?(?:\.\d+)?', price)
                if match:
                    value = match.group()
                    price = Decimal(re.sub(r'[^\d.]', '', value))
            if quality:
                quality = quality[0].text.strip()
            if UoM:
                UoM = UoM[0].text.strip()
            
            temp['title'] = title         
            temp['price'] = float(price)
            temp['link'] = link
            temp['quality'] = quality
            temp['uom'] = UoM
            temp['currency'] = "USD"

            data.append(temp)
            
    return data