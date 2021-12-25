# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

user_name = input('Input user name: ')
service = 'https://api.github.com/users/' + user_name + '/repos'
req = requests.get(service)
data = json.loads(req.text)

print(data)
with open('repo_user_gh.json', 'w') as f:
    json.dump(data, f)

with open('repo_user_gh.json') as f:
    print(f.read())

# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
# Не поняла задача - какой ответ сервера записать в файл? пишу так же в json. Ну и еще красивенький вывод некоторой инфы
# Поскольку болею, пошла максимально простым путем: создала токен на github и получу оттуда количество приват. репоз-ев

user_name = 'buzumko'
token = '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'
service = 'https://api.github.com/user/'
req = requests.get('https://api.github.com/user', auth=(user_name, token))
data = json.loads(req.text)
print(f'Количество приватных репозиториев: {data["total_private_repos"]}; использование диска: {data["disk_usage"]}; '
      f'соавторы: {data["collaborators"]}')
with open('user_gh.json', 'w') as f:
    json.dump(data, f)

with open('user_gh.json') as f:
    print(f.read())
