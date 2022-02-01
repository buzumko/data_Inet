# 1) Написать приложение, которое будет проходиться по указанному списку двух и/или более пользователей
# и собирать данные об их подписчиках и подписках.
# 2) По каждому пользователю, который является подписчиком
# или на которого подписан исследуемый объект нужно извлечь имя, id, фото
# (остальные данные по желанию). Фото можно дополнительно скачать.
# 4) Собранные данные необходимо сложить в базу данных. Структуру данных нужно заранее продумать, чтобы:
# 5) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
# 6) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь


import scrapy
import json
import re
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from instascraper.items import InstascraperItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'
    inst_passw = '#PWD_INSTAGRAM_BROWSER:10:1643131213:AZZQAGTPs6xfu+lt7ppOoFuIqKbWrZ4VaEX53g+SZCn8PJlFrepy7g4RoBJ9hG8g+yNb2R3TWGMrJek2u4SWHgpXYJPp7CijVJirea6j+tAGshfXR9HonVrpXtM9HF0oH+v2RlGNdeDqkBSgLuKb'
    user_for_parse = 'ai_machine_learning'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_passw},
                                 headers={'X-CSRFToken': csrf_token})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(f'/{self.user_for_parse}',
                                  callback=self.user_parse,
                                  cb_kwargs={'username': self.user_for_parse})

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'first': 12}
        url = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
        yield response.follow(url,
                              callback=self.user_posts_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)})

    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')

            url = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'

            yield response.follow(url,
                                  callback=self.user_posts_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)})

        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        for post in posts:
            item = InstascraperItem(
                user_id=user_id,
                username=username,
                photo=post.get('node').get('display_url'),
                likes=post.get('node').get('edge_media_preview_like').get('count'),
                post_data=post.get('node')
            )
            yield item

        # product.add_xpath('product_specifications_names', "//dl[@class='def-list']/dd/text()")
        # product.add_xpath('product_specifications_values', "//dl[@class='def-list']/dt/text()")

    def fetch_csrf_token(self, text):
        # Get csrf-token for auth
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        try:
            matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]

