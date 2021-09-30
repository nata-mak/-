# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность)
# с сайтов HH(обязательно) и/или Superjob(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# - Наименование вакансии.
# - Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# - Ссылку на саму вакансию.
# - Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.

# https://hh.ru/vacancies/data-scientist

import requests
from pprint import pprint
import pandas as pd
from bs4 import BeautifulSoup as bs

url = 'https://hh.ru'
speciality = '/vacancies/data-scientist'
full_url = url + speciality
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
vacancies = []
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
                salary_max = salary[1]
                salary_min = None
            elif salary[0] == 'от':
                salary_min = salary[1]
                salary_max = None
            else:
                salary_min = salary[0]
                salary_max = salary[2]
            currency = salary[-1]

    # работодатель:
        prof_employer = prof.find('div', attrs={'class':'vacancy-serp-item__meta-info-company'}).text
    # сайт, откуда собрана вакансия - указываем url

        prof_data['Вакансия'] = prof_name
        prof_data['Ссылка на вакансию'] = prof_link
        prof_data['Мин. зарплата'] = salary_min
        prof_data['Макс. зарплата'] = salary_max
        prof_data['Валюта'] = currency
        prof_data['Работодатель'] = prof_employer
        prof_data['Сайт'] = url

        vacancies.append(prof_data)
# Переход на следующую страницу:
    next_page = soup.find('a', attrs={'class':'bloko-button', 'data-qa':'pager-next'})
    if next_page:
        full_url = url + next_page['href']
    else:
        break

#pprint(len(vacancies))

# Оформляем результат с помощью DataFrame и сохраняем в файл:
d = pd.DataFrame(vacancies)
d.to_csv('Hh_ru', sep=";", index=False)
