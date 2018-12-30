# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class FeixiaohaoExchangeItem(Item):

    exchange_name = Field()
    last_updated_timestamp = Field()
    volume_cny = Field()
    pairs_amount = Field()
    country = Field()
    transaction_type = Field()
    stars = Field()
    meta = Field()
    unique_id = Field()


class FeixiaohaoConcept(Item):

    unique_id = Field()
    last_updated_timestamp = Field()
    concept = Field()
    volume_cny = Field()
    average_change = Field()
    best = Field()
    worst = Field()
    pairs_amount = Field()
    rise_fall = Field()

