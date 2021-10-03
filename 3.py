# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию.
# Добавить в решение со сбором вакансий функцию,
# которая будет добавлять только новые вакансии в вашу базу.

import requests
from pprint import pprint
import pandas as pd
from bs4 import BeautifulSoup as bs
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

url = 'https://hh.ru'
speciality = '/vacancies/data-scientist'
full_url = url + speciality
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
vacancies = []

# Создание БД и подключение к MongoDB:
client = MongoClient('127.0.0.1', 27017)
db = client['Vacancies']
offer = db.offer  # создание коллекции

while True:
    response = requests.get(full_url, headers=headers)
    soup = bs(response.text, 'html.parser')
    prof_list = soup.find_all('div', attrs={'class':'vacancy-serp-item'})
    if not prof_list or not response.ok:
        break

    for prof in prof_list:
        prof_data = {}
        prof_info_name_link = prof.find('a', attrs={'class':'bloko-link', 'data-qa':'vacancy-serp__vacancy-title'})
    # Наименование и ссылка на вакансию:
        prof_name = prof_info_name_link.text
        prof_link = prof_info_name_link['href']
    # зарплата:
        prof_salary = prof.find('span', attrs={'class':'bloko-header-section-3', 'data-qa':'vacancy-serp__vacancy-compensation'})
        if not prof_salary:
            salary_min = None
            salary_max = None
            currency = None
        else:
            salary = prof_salary.text
            salary = salary.replace('\u202f', '').split(' ')

            if salary[0] == 'до':
                salary_max = int(salary[1])
                salary_min = None
            elif salary[0] == 'от':
                salary_min = int(salary[1])
                salary_max = None
            else:
                salary_min = int(salary[0])
                salary_max = int(salary[2])
            currency = salary[-1]

    # работодатель:
        prof_employer = prof.find('div', attrs={'class':'vacancy-serp-item__meta-info-company'}).text
    # сайт, откуда собрана вакансия - указываем url

        prof_data['Вакансия'] = prof_name
        prof_data['Ссылка на вакансию'] = prof_link
        prof_data['Мин_зарплата'] = salary_min
        prof_data['Макс_зарплата'] = salary_max
        prof_data['Валюта'] = currency
        prof_data['Работодатель'] = prof_employer
        prof_data['Сайт'] = url

        vacancies.append(prof_data)

# ДОБАВЛЕНИЕ ТОЛЬКО НОВЫХ ВАКАНСИЙ В БД:
        try:
            offer.insert_one(prof_data)
            offer.create_index('Ссылка на вакансию', unique=True)
        except dke:
            continue

# Переход на следующую страницу:
    next_page = soup.find('a', attrs={'class':'bloko-button', 'data-qa':'pager-next'})
    if next_page:
        full_url = url + next_page['href']
    else:
        break

# pprint(len(vacancies))

# Оформляем результат с помощью DataFrame и сохраняем в файл:
d = pd.DataFrame(vacancies)
d.to_csv('Hh_ru', sep=";", index=False)

# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
# больше введённой суммы (необходимо анализировать оба поля зарплаты):

def salary_gt():
    summa = int(input('Введите желаемую зарплату: '))
    finder = {'$or': [
        {'Мин_зарплата': {'$gt': summa}},
        {'Макс_зарплата': {'$gt': summa}}
        ]
        }
    result = offer.find(finder)
    print(f'Найдено {offer.count(finder)} вакансий: ')
    for i in result:
        pprint(i)

#salary_gt()


