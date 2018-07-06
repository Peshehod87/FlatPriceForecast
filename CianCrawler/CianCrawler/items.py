# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
from  scrapy import Item, Field
from scrapy.loader.processors import MapCompose

FLAT_FLOOR = 0
ALL_FLOORS = 1

def extruct_numeric(str):
    match  = re.search(r'-?\d+[,]?\d*',str)
    if(match):
        return match.group(0)
    return None

def extruct_remoteness_type(str):
    strippedStr =  re.sub('\s+', ' ', str.strip())
    return re.sub(r'\d+ мин. ','',strippedStr)

def get_floor(group):
    def process(value):
        match  = re.findall(r'\d+',value)
        if(match):
            return match[group]

    return process

class FlatItem(Item):
    underground = Field()
    remoteness = Field(input_processor=MapCompose(extruct_numeric))
    remotenessType = Field(input_processor=MapCompose(extruct_remoteness_type))

    address = Field() #possible it should be AddressItem
    city = Field()
    district = Field()
    street = Field()
    house = Field()

    roomsNumber = Field(input_processor=MapCompose(extruct_numeric))
    squareTotal = Field(input_processor=MapCompose(extruct_numeric))
    squareLive = Field(input_processor=MapCompose(extruct_numeric))
    squareKitchen = Field(input_processor=MapCompose(extruct_numeric))
    price = Field(input_processor=MapCompose(lambda str: re.sub(r'р\.','',str.strip())))
    flatFloor = Field(input_processor=MapCompose(get_floor(FLAT_FLOOR)))
    floorsCount = Field(input_processor=MapCompose(get_floor(ALL_FLOORS)))
    description = Field()
    additionalInfo = Field()


class AddressItem(Item):
    pass