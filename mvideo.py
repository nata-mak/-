#Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.
#Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  #Отвечает за задержку при загрузке страницы
from selenium.webdriver.support import expected_conditions as EC  #Отвечает за ожидание событий
import time
from selenium.common import exceptions as se
from pprint import pprint
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

# Создание БД и подключение к MongoDB:

client = MongoClient('127.0.0.1', 27017)
db = client['M_Video']
trend = db.trend  #создание коллекции

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.get("https://www.mvideo.ru/")
wait = WebDriverWait(driver, 20)

#Убираем всплывающее окно:
btn = wait.until(EC.presence_of_element_located((By.XPATH, '//mvid-icon[contains(@class, "modal-layout__close ng-tns-c72-1 ng-star-inserted")]')))
btn.click()
time.sleep(4)

#Прокрутка на высоту экрана до нужного раздела:
driver.execute_script("window.scrollTo(0, 1500);")
time.sleep(4)

element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//mvid-shelf-group/*//span[contains(text(), 'В тренде')]")))
element.click()

# Прокрутка товаров в разделе "В тренде":
while True:
    try:
        button = driver.find_elements(By.XPATH, '//mvid-shelf-group/*//button[contains(@class, "btn forward")]/mvid-icon[@type = "chevron_right"]')
        button[1].click()
        time.sleep(3)
    except se.ElementNotInteractableException:
        break

# Собираем инфо о товарах:
items = driver.find_elements(By.XPATH, "//mvid-shelf-group//mvid-product-cards-group//div[@class='title']")
#print(len(items))

items_list = []
for item in items:
    item_info = {}
    item_link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
    item_title = item.find_element(By.TAG_NAME, "a").text
    item_info['Title'] = item_title
    item_info['Link'] = item_link

    items_list.append(item_info)
# Добавление в БД Mongo:
    try:
        trend.insert_one(item_info)
        trend.create_index('Link', unique=True)
    except dke:
        continue

pprint(items_list)
driver.close()



