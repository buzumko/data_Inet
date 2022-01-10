# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность)
# с сайтов HH(обязательно) и/или Superjob(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.
# !!!Сделала не все, но по состоянию здоровья не успеваю.
# И еще сменила регион в ходе написания, чуть не рехнулась с загрузкой страницы

from bs4 import BeautifulSoup
import requests
from pprint import pprint
import pandas as pd

job_name = input('Введите название вакансии:') # data-scientist
# https://hh.ru/vacancies/data-scientist
# https://hh.ru/vacancies/data-scientist?customDomain=1
# <div class="vacancy-serp-item" data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus">
url = 'https://hh.ru/vacancies/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/96.0.4664.110 Safari/537.36'}
params = {'customDomain':'1'}

response = requests.get(url+job_name, params=params, headers=headers)
soup = BeautifulSoup(response.text,'html.parser')
vacancies = soup.select('.vacancy-serp-item__row_header')
# vacancies = soup.find_all('div', {'class':'vacancy-serp-item'})

vacancies_list = []

for vacancy in vacancies:
    vacancy_data = {}
    info = vacancy.find('a', {'class': 'bloko-link'})
    name = info.text
    # print(name)
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
            salary_max = -2 # так обозначаю отсутсвие верхней границы
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
    vacancies_list.append(vacancy_data)


pprint(vacancies_list)
b = pd.DataFrame(vacancies_list)
b.to_csv("vacancies.csv", sep=";", index=False)
