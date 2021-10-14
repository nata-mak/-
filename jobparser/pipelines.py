# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy import item

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancytask

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary_hhru(item['salary'])
            del item['salary']
        else:
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary_sjru(item['salary'])
            del item['salary']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hhru(self, salary):
        if salary == ['з/п не указана']:
            salary_min = None
            salary_max = None
            currency = None
        else:
            if salary[0] == 'до ':
                salary_max = int(salary[1].replace('\xa0', ''))
                salary_min = None
            elif (salary[0] == 'от ') and ((' до ') not in salary):
                salary_min = int(salary[1].replace('\xa0', ''))
                salary_max = None
            else:
                salary_min = int(salary[1].replace('\xa0', ''))
                salary_max = int(salary[3].replace('\xa0', ''))
        # обработка валюты:
            if 'руб.' in salary:
                currency = 'руб.'
            elif 'USD' in salary:
                currency = 'USD'
            else:
                currency = 'EUR'

        return salary_min, salary_max, currency

    def process_salary_sjru(self, salary):
        if salary == ['По договорённости']:
            salary_min = None
            salary_max = None
            currency = None
        else:
            if salary[0] == 'до':
                salary = salary[2].split('\xa0')
                salary_max = int(salary[0]+salary[1])
                salary_min = None
                currency = salary[-1]

            elif salary[0] == 'от':
                salary = salary[2].split('\xa0')
                salary_min = int(salary[0] + salary[1])
                salary_max = None
                currency = salary[-1]
            else:
                salary_min = int(salary[0].replace('\xa0', ''))
                salary_max = int(salary[1].replace('\xa0', ''))
                currency = salary[-1]
        return salary_min, salary_max, currency

# Варианты на sjru:
# 'salary': ['от', '\xa0', '15\xa0000\xa0руб.']}
# 'salary': ['до', '\xa0', '100\xa0000\xa0руб.']}
# 'salary': ['240\xa0000', '300\xa0000', '\xa0', 'руб.']}
# 'salary': ['По договорённости']}

# Варианты зп на hh.ru:
# 'salary': ['от ', '120\xa0000', ' до ', '200\xa0000', ' ', 'руб.', ' на руки'],
# 'salary': ['от ', '70\xa0000', ' ', 'руб.', ' на руки'],
# 'salary': ['до ', '270\xa0000', ' ', 'руб.', ' на руки'],
# 'salary': ['з/п не указана']
