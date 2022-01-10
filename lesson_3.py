# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии/продукты в вашу базу.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).


from bs4 import BeautifulSoup
import requests
from pprint import pprint
from pymongo import MongoClient


# Функция, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
def get_vacansies_more_value(value, cur_value):
    for doc in vacancy_db.find({'salary_currency': cur_value, '$or': [{'salary_min': {'$gte': value}}, {'salary_max': {'$gte': value}}]}):
        pprint(doc)


# job_name = input('Введите название вакансии:') # data-scientist
job_name = 'data-scientist'
# https://hh.ru/vacancies/data-scientist?customDomain=1
# <div class="vacancy-serp-item" data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus">
url = 'https://hh.ru/vacancies/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/96.0.4664.110 Safari/537.36'}
params = {'customDomain':'1'}

response = requests.get(url+job_name, params=params, headers=headers)
soup = BeautifulSoup(response.text,'html.parser')
vacancies = soup.select('.vacancy-serp-item__row_header')

# vacancies_list = []
client = MongoClient('127.0.0.1', 27017)
db = client['vacancies_database_1']
vacancy_db = db.vacancies

for vacancy in vacancies:
    vacancy_data = {}
    info = vacancy.find('a', {'class': 'bloko-link'})
    name = info.text
    link = url + info.get('href')
    salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary_list = []
    salary_min = -1  # -1 обозначает, что информации нет
    salary_max = -1  # -1 обозначает, что информации нет
    salary_currency = 'руб.'
    if salary:
        salary_list = salary.getText().split()
        if salary_list[0].lower() == 'до':
            salary_max = int(salary_list[1] + salary_list[2])
            salary_currency = salary_list[3]
        elif salary_list[0].lower() == 'от':
            salary_min = int(salary_list[1] + salary_list[2])
            salary_max = -2  # так обозначаю отсутсвие верхней границы
            salary_currency = salary_list[3]
        else:
            salary_min = int(salary_list[0] + salary_list[1])
            salary_max = int(salary_list[3] + salary_list[4])
            salary_currency = salary_list[5]

    vacancy_data['name'] = name
    vacancy_data['salary_min'] = salary_min
    vacancy_data['salary_max'] = salary_max
    vacancy_data['salary_currency'] = salary_currency
    vacancy_data['link'] = link
    count = vacancy_db.count_documents({'link': link})
    if count == 0:
        vacancy_db.insert_one(vacancy_data)
        print('Add')
    # vacancies_list.append(vacancy_data)

print(f'Всего записей в базе: {vacancy_db.count_documents({})}')

# Часть 2
user_cur_value = input('Введите валюту (руб., EUR, USD):')  # руб.
user_value = int(input('Введите желаемую зарплату (целое число):'))  # 70000
get_vacansies_more_value(user_value, user_cur_value)
