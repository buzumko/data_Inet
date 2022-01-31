# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def clear_price(value):
    try:
        value = int(value.replace(' ', ''))
    except:
        pass
    return value


class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(default=None, output_processor=TakeFirst(), input_processor=MapCompose(clear_price))
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
