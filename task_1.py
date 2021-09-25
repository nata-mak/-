# Посмотреть документацию к API GitHub, разобраться как вывести
# список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
#https://api.github.com/users/USERNAME/repos

import requests
from pprint import pprint
import json
username = input("Введите имя пользователя: ")

response = requests.get('https://api.github.com/users/' + username + '/repos')
j_data = response.json()

for i in j_data:
    pprint(i['name'])

with open('j_data.json', 'w') as f:
    json.dump(j_data, f)