from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd 
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


url="https://www.flipkart.com/"

driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()
sleep(1)

input_search = driver.find_element(By.CLASS_NAME,"Pke_EE")
input_search.send_keys("Shoes")

search_button = driver.find_element(By.CLASS_NAME, "_2iLD__")
search_button.click()

elements = driver.find_elements(By.CLASS_NAME,"ukzDZP")
first_element = elements[0]
first_element.click()

gender = driver.find_elements(By.CLASS_NAME, "XqNaEv")
women = gender[1]
women.click()
sleep(15)

brand = driver.find_elements(By.CLASS_NAME,"XqNaEv")
nike = brand[3]
nike.click()
sleep(15)

pname = []
price = []
discount = []
all_names = []
all_prices = []
all_discounts = []
next = driver.find_element(By.CLASS_NAME, "_9QVEpD")

for i in range(1,21):
    #boxes = driver.find_elements(By.CLASS_NAME, "._1sdMkc.LFEi7Z")
    wait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "._1sdMkc.LFEi7Z")))

    names = driver.find_elements(By.CLASS_NAME, "WKTcLC")
    prices = driver.find_elements(By.CLASS_NAME, "yRaY8j")
    discounts = driver.find_elements(By.CLASS_NAME, "Nx9bqj")

    pname = [name.text for name in names]
    pprice = [price.text if price.text else "NA" for price in prices]
    pdiscount = [discount.text if discount.text else "NA" for discount in discounts]

    while len(pdiscount) < len(pname):
        pdiscount.append("NA")
    
    while len(pprice) < len(pname):
        pprice.append("NA")

    all_names.extend(pname)
    all_prices.extend(pprice)
    all_discounts.extend(pdiscount)

    next.click()

    sleep(15)

df=pd.DataFrame({"ProductName":all_names,"ProductPrice":all_prices, "ProductDiscount":all_discounts})
df.to_csv("nike_women.csv")