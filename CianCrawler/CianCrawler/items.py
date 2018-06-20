# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from  scrapy import Item, Field


class FlatItem(Item):
    underground = Field()
    remoteness = Field()
    remotenessType = Field()
    address = Field() #possible it should be AddressItem
    objectType = Field()
    square = Field()
    price = Field()
    floor = Field()
    description = Field()
    additionalInfo = Field()


class AddressItem(Item):
    pass