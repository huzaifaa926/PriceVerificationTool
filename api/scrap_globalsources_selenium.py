from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
from config import *
# from decimal import Decimal
import locale
locale.setlocale(locale.LC_ALL, '')

logging.basicConfig(filename='../logs/app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d %b, %Y %H:%M:%S', level=LOG_LEVEL)

options = Options()
options.add_argument("--headless")

def normalize_url(url):
    if url.startswith('//'):
        url = url[2:]
    elif url.startswith('/'):
        url = url[1:]

    if not url.startswith('https://'):
        url = 'https://' + url

    return url


def clean_title(title):
    try:
        title = title.text.strip()
    except Exception as e:
        logging.error(f"{'-'*10} In clean_title function {'-'*10}")
        logging.error(e)
        title = None
    return title

def clean_price_uom(price_html):
    # price_html = BeautifulSoup(price_html, 'lxml')
    # Handles cases where there are multiple prices available for a product
    try:
        price = price_html.find('div', class_='swiper-money-container').text.strip()
        uom = price_html.find('span', class_='unit').text.strip()

        # price = float(Decimal(re.sub(r'[^(\d.)]', '', price)))
        price = locale.atof(re.search(r'\$([\d,]+\.\d+)', price).group(1))
        uom = re.sub(r'[\d\W_]+', '', uom)
        return price, uom
    except Exception as e:
        logging.error(f"{'-'*10} In clean_price_uom function 1st exception {'-'*10}")
        logging.error(e)

    # Handles cases where there is a price range available for a product
    try:
        price = price_html.find('tr', class_='only-one-priceNum-tr').find_all('span')[0].text.strip()
        uom = price_html.find('tr', class_='only-one-priceNum-tr').find_all('span')[1].text.strip()
        
        # price = float(Decimal(re.search(r'\$(\d+\.\d+)', price).group(1)))
        price = locale.atof(re.search(r'\$([\d,]+\.\d+)', price).group(1))
        uom = re.sub(r'[\d\W_]+', '', uom)
        return price, uom
    except Exception as e:
        logging.error(f"{'-'*10} In clean_price_uom function 2nd exception {'-'*10}")
        logging.error(e)
    
    return 0, 0

def scrap(keyword):
    logging.info("-"*50)
    logging.info(f"Scrapping for {keyword}")
    keyword = urllib.parse.quote(keyword)
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://www.made-in-china.com/productdirectory.do?subaction=hunt&style=b&mode=and&code=0&comProvince=nolimit&order=0&isOpenCorrection=1&org=top&keyword=&file=&searchType=0&word={keyword}')
    html = driver.page_source
    driver.close()

    soup = BeautifulSoup(html, 'lxml')
    product_lists = soup.find('div', {'class': 'prod-list'}).findChildren("div" , recursive=False)
    data = []
    for product in product_lists[:LIMIT]:
        temp = {}
        if product.find('h2'):
            try:
                link = product.find('h2').find('a')['href']
                link = normalize_url(link)
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
                response=requests.get(link, headers=headers)
                soup=BeautifulSoup(response.text,'lxml')
                title = soup.find('div', {'class':'sr-proMainInfo-baseInfo-name'})
                price_html = soup.find('div', {'class':'sr-proMainInfo-baseInfo-propertyPrice'})

                logging.info(f"{keyword} : {link}")
                temp['title'] = clean_title(title)
                temp['price'], temp['uom'] = clean_price_uom(price_html)
                temp['link'] = link
                temp['currency'] = "USD"

                data.append(temp)
                print(temp)
            except Exception as e:
                logging.error(f"{'-'*10} In product list loop {'-'*10}")
                logging.error(e)
                logging.error(f"{keyword} : {link}")
                
            
    return data


scrap("ball bearings")
# clean_price_uom('<div class="sr-proMainInfo-baseInfo-propertyPrice"><div class="only-one-priceNum" style="padding: 15px"><table><tbody><tr class="only-one-priceNum-tr" style="display: inline-flex;align-items: baseline; flex-wrap: wrap;"><td style="padding: 0 !important;"><span style="font-size: 20px;font-family: Roboto, Roboto-Bold;font-weight: 700;text-align: left;color: #e64545;padding-left: 0 !important;">US $0.40</span><span style="font-size: 14px;font-family: Roboto, Roboto-Regular;font-weight: 400;color: #888888;margin-right: 10px;">/ Set</span><span style="color: #e6ecf2;">|</span></td><td class="sa-only-property-price only-one-priceNum-price"><span>10 Sets</span><span style="color: #888888">(Min. Order)</span></td></tr></tbody></table></div></div>')
# clean_price_uom('<div class="sr-proMainInfo-baseInfo-propertyPrice">                                            <div style="padding: 15px" class="only-one-priceNum">                            <table>                                <tbody>                                <tr style="display: inline-flex;align-items: baseline; flex-wrap: wrap;" class="only-one-priceNum-tr">                                    <td style="padding: 0 !important;">                                        <span style="                                        font-size: 20px;                                        font-family: Roboto, Roboto-Bold;                                        font-weight: 700;                                        text-align: left;                                        color: #e64545;                                        padding-left: 0 !important;">US $0.10-2.00</span>                                        <span style="font-size: 14px;font-family: Roboto, Roboto-Regular;font-weight: 400;color: #888888;margin-right: 10px;">/ Piece</span>                                        <span style="color: #e6ecf2;">|</span>                                    </td>                                    <td class="sa-only-property-price only-one-priceNum-price">                                       <span>1,000 Pieces</span>                                        <span style="color: #888888">                                            (Min. Order)                                        </span>                                    </td>                                </tr>                                </tbody>                            </table>                        </div>                </div>')
# clean_price_uom('<div class="sr-proMainInfo-baseInfo-propertyPrice">                                        <div id="swiper-container" class="swiper-container-div">                        <div class="swiper-wrapper-div">                                                                    <div class="swiper-slide-div">                                        <div class="swiper-money-container">US $2.00</div>                                        <div class="swiper-unit-container">100-999 <span class="unit">Pieces</span></div>                                    </div>                                                                    <div class="swiper-slide-div">                                        <div class="swiper-money-container">US $1.50</div>                                        <div class="swiper-unit-container">1,000+ <span class="unit">Pieces</span></div>                                    </div>                        </div>                    </div>                </div>')

# clean_price_uom('<div class="product-price" data-auto-exp="module_price"><div class="price-list"><div class="price-item"><div class="quality">1 - 4 sets</div><div class="price"><span class="promotion">$14,500.00</span></div></div><div class="price-item"><div class="quality">5 - 9 sets</div><div class="price"><span class="">$14,000.00</span></div></div><div class="price-item"><div class="quality">10 - 99 sets</div><div class="price"><span class="">$13,700.00</span></div></div><div class="price-item"><div class="quality">&gt;= 100 sets</div><div class="price"><span class="">$6,800.00</span></div></div></div></div>')
# clean_price_uom('<div class="product-price" data-auto-exp="module_price" data-aplus-clk="x5_18b208be" data-spm-anchor-id="a2700.details.0.i5.566a10a2jPDHWD" data-aplus-ae=""><div class="price-list"><div class="price-range"><span class="price" data-spm-anchor-id="a2700.details.0.i24.566a10a2jPDHWD">$100,000.00 - $200,000.00</span><span class="unit">/ unit |</span><span class="moq">1 unit/units</span><span class="name">(Min. order)</span></div></div></div>')