from lib2to3.pgen2 import driver
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

PATH = 'C:\Program Files (x86)\chromedriver.exe'

driver = webdriver.Chrome(PATH)
url = "https://www.detmir.ru/catalog/index/name/lego/"
driver.get(url)
driver.maximize_window()


for i in range (0,60):
    driver.find_element(By.CSS_SELECTOR,".gM.gQ.g_4.gW.hd.hf.gZ").click()
    time.sleep(3) 

city = driver.find_element(By.CLASS_NAME, 'o_6').text
search = driver.find_elements(By.CLASS_NAME, 'u_9') 

table = []

for element in search:
    new_line = []
    link = element.find_element(By.XPATH,"./a").get_attribute('href')
    id = link[39:-1]
    new_line.append(id)
    split_text = element.text.replace('\u2009', ' ').split('\n')
    for text in split_text:
        try:
             int(text)
        except:
            if '%' in text:
                continue
            if "МЕГА СКИДКИ" == text:
                continue
            if "Только у нас" == text:
                continue
            if "Уведомить о появлении" == text:
                continue
            new_line.append(text)
    new_line.insert(3,city)
    new_line.append(link)
    if new_line[4].startswith('h'):
        new_line.insert(4,' ')
    table.append(new_line)


pd.DataFrame(table).to_csv('output.csv', index=False, header=[
    'ID товара',
    'Наименование',
    'Цена',
    'Город',
    'Промо цена (если имеется)',
    'Ссылка на страницу с товаром'])   
driver.close()