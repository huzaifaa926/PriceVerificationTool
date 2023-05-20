from bs4 import BeautifulSoup
import requests
import base64
import json


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

url = 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=ball%20bearing&viewtype=G&page=1'

response=requests.get(url, headers=headers)



soup=BeautifulSoup(response.text,'lxml')
print(len(soup.find_all(attrs={'data-role': 'item'})))


#print(len(soup.find("div", { "class" : "organic-list" })))

# for item in soup.select('.organic-list'):
# 	try:
# 		print('----------------------------------------')
# 		print(item)
# 	except Exception as e:
# 		#raise e
# 		print('')