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
    inst_login = 'buzumka1979@yandex.ru'
    inst_passw = '#PWD_INSTAGRAM_BROWSER:10:1643805250:AahQABf/BR6mymtrBKWpEPSIfKb00tHMuRjloS5PQkD2Ky9Hpliijmfu09dBelz7/' \
                 'FIGlsXCu7M6AXtMo/TfDQg6izoyOEE9ZFgyOsIihEij/QheulaMrbVOnxnyp4Nkekb69I8Ep8cG+TP91Kn93Ria8d9dMBY='
    user_for_parse = ['timour1444', 'konstantindocv']
    api_url = 'https://i.instagram.com/api/v1/friendships/'
    followers_hash = '8c2a529969ee035a5063f2fc8602a0fd'

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
            for user in self.user_for_parse:
                yield response.follow(f'/{user}',
                                      callback=self.user_parse,
                                      cb_kwargs={'username': user})

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        # type_user = ['followers', 'following']

        type_u = 'followers'
        variables = {'count': 12,
                     'max-id': 12,
                     'search_surface': 'follow_list_page'}
        url = f'{self.api_url}{user_id}/{type_u}/?{urlencode(variables)}'
        # print(url)
        yield response.follow(url,
                              callback=self.user_followers_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'type_user_fol': type_u,
                                         'variables': deepcopy(variables)},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        # for type_u in type_user:
        #     if type_u == 'followers':
        #         variables = {'count': 12,
        #                      'max-id': 12,
        #                      'search_surface': 'follow_list_page'}
        #         url = f'{self.api_url}{user_id}/{type_u}/?{urlencode(variables)}'
        #         # print(url)
        #         yield response.follow(url,
        #                               callback=self.user_followers_parse,
        #                               cb_kwargs={'username': username,
        #                                          'user_id': user_id,
        #                                          'type_user_fol': type_u,
        #                                          'variables': deepcopy(variables)},
        #                               headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        #     else:
        #         variables = {'count': 12,
        #                      'max-id': 12}
        #         url = f'{self.api_url}{user_id}/{type_u}/?{urlencode(variables)}'
        #         # https: // i.instagram.com / api / v1 / friendships / 47601635336 / followers /?count = 12 & max_id = 12 & search_surface = follow_list_page
        #         # print(url)
        #         yield response.follow(url,
        #                               callback=self.user_following_parse,
        #                               cb_kwargs={'username': username,
        #                                          'user_id': user_id,
        #                                          'type_user_fol': type_u,
        #                                          'variables': deepcopy(variables)},
        #                               headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def user_followers_parse(self, response: HtmlResponse, username, user_id, type_user_fol, variables):
        # print(username, user_id, variables)
        j_data = response.json()
        users = j_data.get('users')
        for user in users:
            item = InstascraperItem(
                user_id_main=user_id,
                user_main_name=username,
                user_id_fol=user.get('pk'),
                user_fol_name=user.get('username'),
                user_status=type_user_fol,
                user_fol_foto_url=user.get('profile_pic_url'),
            )
            yield item

        page_info = j_data.get('big_list')

        if page_info:
            variables['max-id'] = variables['max-id'] + 12
            url = f'{self.api_url}{user_id}/{type_user_fol}/?{urlencode(variables)}'
            yield response.follow(url,
                                  callback=self.user_followers_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'type_user_fol': type_user_fol,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})




    # def user_following_parse(self, response: HtmlResponse, username, user_id, type_user_fol, variables):
    #     print(username, user_id, variables)
    #     j_data = response.json()
    #
    #     page_info = j_data.get('big_list')
    #     if page_info:
    #         variables['max-id'] = variables['max-id'] + 12
    #         url = f'{self.api_url}{user_id}/{type_user_fol}/?{urlencode(variables)}'
    #         yield response.follow(url,
    #                               callback=self.user_following_parse,
    #                               cb_kwargs={'username': username,
    #                                          'user_id': user_id,
    #                                          'type_user_fol': type_user_fol,
    #                                          'variables': deepcopy(variables)},
    #                               headers={'User-Agent': 'Instagram 155.0.0.37.107'})
    #
    #     users = j_data.get('users')
    #     for user in users:
    #         item = InstascraperItem(
    #             user_main_id=user_id,
    #             user_main_name=username,
    #             user_fol_id=user.get('pk'),
    #             user_fol_name=user.get('username'),
    #             user_status=type_user_fol,
    #             user_fol_foto_url=user.get('profile_pic_url')+user.get('profile_pic_id')
    #         )
    #         yield item


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

