# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru.
# Для парсинга использовать XPath. Структура данных должна содержать:
# - название источника;
# - наименование новости;
# - ссылку на новость;
# - дата публикации.
# 2. Сложить собранные новости в БД

# 2) переходим на страницу новости и собираем данные

from lxml import html
from pprint import pprint
import requests
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

# 1)собираем ссылки на новость:
url = 'https://news.mail.ru/'
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)
top_news = []
main_hrefs = dom.xpath("//a[contains(@class, 'js-topnews__item')]/@href | //li[@class='list__item']/a[@class='list__text']/@href")
#pprint(main_hrefs)

# 2) Создание БД и подключение к MongoDB:

client = MongoClient('127.0.0.1', 27017)
db = client['Top_news_mail_ru']
db_news = db.db_news   #создание коллекции

# 3) переходим на страницу новости и собираем данные:
for href in main_hrefs:
    news = {}
    url_news = href
    response_news = requests.get(url_news, headers=headers)
    dom_news = html.fromstring(response_news.text)
    title = dom_news.xpath("//h1/text()")
    source = dom_news.xpath("//span[@class='note']/a/span[@class='link__text']/text()")
    date = dom_news.xpath("//span[@class='note']/span/@datetime")

    news['Source_name'] = source
    news['Title'] = title
    news['Link'] = href
    news['Publication_date'] = date
    top_news.append(news)

# Добавление в базу данных только новых статей:
    try:
        db_news.insert_one(news)
        db_news.create_index('Link', unique=True)
    except dke:
        continue

pprint(top_news)


