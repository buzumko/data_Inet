# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#
# пока без текста письма, понимаю, что надо зайти на страничку с письмом и дернуть оттуда текст, но не успеваю

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# from selenium.webdriver.common.service import Service
# from selenium.webdriver.common.options import Options
from pymongo import MongoClient
from pprint import pprint


# Активируем базу
client = MongoClient('127.0.0.1', 27017)
db = client['mails_database']
mails_db = db.mails


# chrome_opt = Options()
# chrome_opt.add_arguments('start-maximized')
driver = webdriver.Chrome()   # options=chrome_opt)
driver.get("https://mail.ru/")

# login
element = driver.find_element(By.NAME, 'login')
element.send_keys("study.ai_172")
element.send_keys(Keys.ENTER)

time.sleep(5)

# password
elem = driver.find_element(By.XPATH, "//input[contains(@type,'password')]")
elem.send_keys("NextPassword172#")
elem.send_keys(Keys.ENTER)
# //input[contains(@class,'svelte-1da0ifw')]
# <div class="llc__container">

time.sleep(15)

letters = driver.find_elements(By.XPATH, "//a[contains(@class,'llc_normal')]")
time.sleep(2)


print('stop')
letters_list = []
for letter in letters:
    letter_one = {}
    correspondent_item = letter.find_element(By.CLASS_NAME, 'll-crpt')
    title_item = letter.find_element(By.CLASS_NAME, 'll-sj__normal')
    date_item = letter.find_element(By.CLASS_NAME, 'llc__item_date')
    letter_one['correspondent'] = correspondent_item.text
    letter_one['title'] = title_item.text
    letter_one['date'] = date_item.text
    letter_one['URL'] = letter.get_attribute('href')
    count_n = mails_db.count_documents({'URL':  letter_one['URL']})
    if count_n == 0:
        mails_db.insert_one(letter_one)
        print('Add')
    letters_list.append(letter_one)
# elem.send_keys(Keys.RETURN)
#

# это попытка разлогинится, пока не придумала как
# elem = driver.find_element(By.XPATH, "//span[contains(@class,'ph-dropdown-ic')]")
# element.send_keys(Keys.ENTER)
# time.sleep(1)
#
# element = driver.find_element(By.XPATH, "//a[contains(@href,'logout')]")
# element.send_keys(Keys.ENTER)
# time.sleep(10)

driver.close()

