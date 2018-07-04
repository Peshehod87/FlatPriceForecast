# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
from  scrapy import Item, Field
from scrapy.loader.processors import MapCompose

class FlatItem(Item):
    underground = Field()
    remoteness = Field(input_processor=MapCompose(lambda s: re.sub('\s+', ' ', s.strip())))
    remotenessType = Field()

    address = Field() #possible it should be AddressItem
    city = Field()
    district = Field()
    street = Field()
    house = Field()

    objectType = Field()
    square = Field()
    price = Field(input_processor=MapCompose(lambda str: re.sub('р\.','',str.strip())))
    floor = Field(input_processor=MapCompose(lambda str: re.sub('\s+',' ',str.strip())))
    description = Field(input_processor=MapCompose(lambda str: re.sub('\s+',' ',str.strip())))
    additionalInfo = Field()


class AddressItem(Item):
    pass