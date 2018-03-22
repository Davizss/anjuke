# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Day14Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HouseItem(scrapy.Item):
    hid = scrapy.Field()
    title = scrapy.Field()
    money = scrapy.Field()
    rent_type = scrapy.Field()
    house_type = scrapy.Field()
    area = scrapy.Field()
    location = scrapy.Field()
    level = scrapy.Field()
    image_path = scrapy.Field()


class CnblogItem(scrapy.Item):
    aid = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    industry = scrapy.Field()
    recommend = scrapy.Field()
    nick = scrapy.Field()
    date_pub = scrapy.Field()
    comment = scrapy.Field()
    read_num = scrapy.Field()
