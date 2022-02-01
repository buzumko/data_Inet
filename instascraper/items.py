# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstascraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    photo = scrapy.Field()
    likes = scrapy.Field()
    post_data = scrapy.Field()