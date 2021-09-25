# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import pprint
import json

country = 'ru'
category = 'general'
language = 'ru'
my_params = {
    'api_token': '***',
    'locale': country,
    'categories': category,
    'language': language
}

# API- сервис для получения актуальных новостей:

url = 'https://api.thenewsapi.com/v1/news/top'
response = requests.get(url, params=my_params)
j_data = response.json()

print('Топ новостей:')
for i in j_data.get('data'):
    print(i['title'])

with open('news_file.json', 'w') as f:
    json.dump(j_data, f)

