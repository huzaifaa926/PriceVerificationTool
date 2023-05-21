from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


options = Options()
options.add_argument("--headless")
# options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path="./chromedriver.exe")

driver.get("https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=ball%20bearing&viewtype=G&page=1")

products_list = driver.find_element(By.CLASS_NAME, "app-organic-search__list")

products = products_list.find_elements(By.CSS_SELECTOR, "div")

# Print the content of each child div
for product in products[:1]:
    print("*"*100)
    print(product.text)
    a = product.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div/h2/a")
    print(a.text)
    print(a.get_attribute("href"))
    print(a.get_attribute("title"))



driver.close()