# Написать приложение, которое собирает основные новости с сайта lenta.ru.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника; - не поняла, о чем речь. Т.к. собирала с одного сайта, не стала всем присаивать один источник
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД

import requests
from pprint import pprint
from pymongo import MongoClient
from lxml import html


# https://lenta.ru/
url = 'https://lenta.ru/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/96.0.4664.110 Safari/537.36'}
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

# Активируем базу
client = MongoClient('127.0.0.1', 27017)
db = client['news_database']
news_db = db.news

# Собираем данные
items = dom.xpath("//a[contains(@class,'card-big')]")
news_url = dom.xpath("//a[contains(@class,'card-big')]/@href|"
                     "//a[contains(@class,'card-mini')]/@href")
count = 0

for item in items:
    news_one = {}
    news_title = item.xpath(".//h3[contains(@class,'card-big__title')]/text()")
    news_time = item.xpath(".//time[contains(@class,'card-big')]/text()")
    news_one['title'] = news_title[0]
    news_one['URL'] = news_url[count]
    news_one['time'] = news_time[0]
    # news.append(news_one)
    count_n = news_db.count_documents({'URL': news_url[count]})
    if count_n == 0:
        news_db.insert_one(news_one)
        print('Add')
    count += 1

items = dom.xpath("a[contains(@class,'card-mini')]")
for item in items:
    news_one = {}
    news_title = item.xpath(".//span[contains(@class,'card-mini__title')]/text()")
    news_time = item.xpath(".//time[contains(@class,'card-mini')]/text()")
    news_one['title'] = news_title[0]
    news_one['URL'] = news_url[count]
    news_one['time'] = news_time[0]
    count_n = news_db.count_documents({'URL': news_url[count]})
    if count_n == 0:
        news_db.insert_one(news_one)
        print('Add')
    count += 1
    # news.append(news_one)

# Первый вариант, но не пошли ссылки
# items = dom.xpath("//a[contains(@class,'card-big')]|//a[contains(@class,'card-mini')]")
# for item in items:
#     news_one = {}
#     news_title = item.xpath(".//h3[contains(@class,'card-big__title')]/text()|"
#                             ".//span[contains(@class,'card-mini__title')]/text()")
#     news_url = item.xpath(".//a[contains(@class,'card-big')]/@href"
#                           "|.//a[contains(@class,'card-mini')]/@href")
#     news_time = item.xpath(".//time[contains(@class,'card-big')]/text()|"
#                            ".//time[contains(@class,'card-mini')]/text()")
#     news_one['title'] = news_title
#     news_one['URL'] = news_url
#     news_one['time'] = news_time
#     news.append(news_one)

pprint(f'Всего записей в базе: {news_db.count_documents({})}')
