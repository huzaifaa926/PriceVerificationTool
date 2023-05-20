from bs4 import BeautifulSoup
import requests
import base64
import json


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

url = 'https://www.globalsources.com/searchList/products?keyWord=ball%20bearing&pageNum=1'
url = 'https://www.made-in-china.com/productdirectory.do?word=ball+bearing&subaction=hunt&style=b&mode=and&code=0&comProvince=nolimit&order=0&isOpenCorrection=1&log_from=4'

response=requests.get(url, headers=headers)




soup=BeautifulSoup(response.text,'lxml')
print(soup)
print(len(soup.find_all(attrs={'class': 'prod-list'})))


#print(len(soup.find("div", { "class" : "organic-list" })))

# for item in soup.select('.organic-list'):
# 	try:
# 		print('----------------------------------------')
# 		print(item)
# 	except Exception as e:
# 		#raise e
# 		print('')