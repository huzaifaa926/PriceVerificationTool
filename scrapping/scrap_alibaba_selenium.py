from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=ball%20bearing&viewtype=G&page=1")

driver.close()