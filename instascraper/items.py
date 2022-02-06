# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstascraperItem(scrapy.Item):
    # define the fields for your item here like:

    user_id_main = scrapy.Field()
    user_main_name = scrapy.Field()
    user_id_fol = scrapy.Field()
    user_fol_name = scrapy.Field()
    user_status = scrapy.Field()
    user_fol_foto_url = scrapy.Field()
