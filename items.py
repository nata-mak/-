# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def int_price(value):
    try:
        value = int(value)
    except:
        return value
    return value

class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(int_price), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()

