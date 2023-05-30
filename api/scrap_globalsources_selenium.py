from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
from decimal import Decimal

LIMIT = 20
options = Options()
# options.add_argument("--headless")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


def normalize_url(url):
    if url.startswith('//'):
        url = url[2:]
    return url.lstrip('/')


def clean_title(title):
    try:
        title = title.text.strip()
    except Exception as e:
        print(e)
        title = None
    return title

def clean_price_uom(price_html):
    # price_html = BeautifulSoup(price_html, 'lxml')
    # Handles cases where there are multiple prices available for a product
    try:
        price = price_html.find_all('div', class_='price-item')[0].find('div', class_='price').text.strip()
        uom = price_html.find_all('div', class_='price-item')[0].find('div', class_='quality').text.strip()

        price = float(re.sub(r'[^(\d.)]', '', price))
        uom = re.sub(r'[\d\W_]+', '', uom)
        return price, uom
    except Exception as e:
        print(e)

    # Handles cases where there is a price range available for a product
    try:
        price = price_html.find('div', class_='price-range').find('span', class_='price').text.strip()
        uom = price_html.find('div', class_='price-range').find('span', class_='unit').text.strip()

        price = float(Decimal(re.search(r'\$(\d+\.\d+)', price).group(1)))
        uom = re.sub(r'[\d\W_]+', '', uom)
        return price, uom
    except Exception as e:
        print(e)
    
    return None, None

def scrap(keyword):
    keyword = urllib.parse.quote(keyword)
    driver = webdriver.Chrome(options=options)
    # driver.get(f"https://www.globalsources.com/searchList/products?fsb=y&IndexArea=product_en&CatId&keyWord={keyword}&viewtype=G&page=1")
    driver.get(f'https://www.made-in-china.com/productdirectory.do?subaction=hunt&style=b&mode=and&code=0&comProvince=nolimit&order=0&isOpenCorrection=1&org=top&keyword=&file=&searchType=0&word={keyword}')
    html = driver.page_source
    driver.close()

    soup = BeautifulSoup(html, 'lxml')
    print(soup)
    product_lists = soup.find('ul', {'class': 'product-list'}).findChildren("li" , recursive=False)
    data = []
    for product in product_lists[:LIMIT]:
        print(product)
        temp = {}
        if product.find('h2'):
            link = product.find('h2').find('a')['href']
            link = 'https://' + normalize_url(link)
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
            response=requests.get(link, headers=headers)
            soup=BeautifulSoup(response.text,'lxml')
            title = soup.find('div', {'class':'product-title'})
            price_html = soup.find('div', {'class':'product-price'})
            
            print(link)
            temp['title'] = clean_title(title)
            temp['price'], temp['uom'] = clean_price_uom(price_html)
            temp['link'] = link
            temp['currency'] = "USD"

            data.append(temp)
            
    return data


scrap("ball bearings")
# clean_price_uom('<div class="product-price" data-auto-exp="module_price"><div class="price-list"><div class="price-item"><div class="quality">50 - 499 pieces</div><div class="price"><span class="promotion">$20.00</span></div></div><div class="price-item"><div class="quality">500 - 1999 pieces</div><div class="price"><span class="">$18.00</span></div></div><div class="price-item"><div class="quality">&gt;= 2000 pieces</div><div class="price"><span class="">$15.00</span></div></div></div></div>')
# clean_price_uom('<div class="product-price" data-auto-exp="module_price"><div class="price-list"><div class="price-item"><div class="quality">50 - 299 pieces</div><div class="price"><span class="promotion">$18.90</span></div></div><div class="price-item"><div class="quality">300 - 499 pieces</div><div class="price"><span class="">$16.90</span></div></div><div class="price-item"><div class="quality">&gt;= 500 pieces</div><div class="price"><span class="">$12.90</span></div></div></div></div>')
# clean_price_uom('<div class="product-price" data-auto-exp="module_price"><div class="price-list"><div class="price-range"><span class="price">$0.24 - $0.80</span><span class="unit">/ piece |</span><span class="moq">200 piece/pieces</span><span class="name">(Min. order)</span></div></div></div>')
# clean_price_uom('<div class="product-price" data-auto-exp="module_price"><div class="price-list"><div class="price-item"><div class="quality">1 - 4 sets</div><div class="price"><span class="promotion">$14,500.00</span></div></div><div class="price-item"><div class="quality">5 - 9 sets</div><div class="price"><span class="">$14,000.00</span></div></div><div class="price-item"><div class="quality">10 - 99 sets</div><div class="price"><span class="">$13,700.00</span></div></div><div class="price-item"><div class="quality">&gt;= 100 sets</div><div class="price"><span class="">$6,800.00</span></div></div></div></div>')