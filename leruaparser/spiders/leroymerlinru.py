# 1) Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
# ● название;
# ● все фото;
# ● ссылка;
# ● цена.
#
# Реализуйте очистку и преобразование данных с помощью ItemLoader. Цены должны быть в виде числового значения.

import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/mebel-dlya-kuhni/']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()  # response.url()[0] +
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[@data-qa="product-image"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photos', '//source[contains(@media, "only screen and (min-width: 768px)")]/@data-origin')
        loader.add_value('url', response.url)
        yield loader.load_item()

# <source media="only screen and (min-width: 768px)" itemprop="image" srcset="https://res.cloudinary.com/lmru/image/
# upload/f_auto,q_auto,w_600,h_600,c_pad,b_white,d_photoiscoming.png/LMCode/82109387.jpg" data-origin="https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_600,h_600,c_pad,b_white,d_photoiscoming.png/LMCode/82109387.jpg" xpath="1">
