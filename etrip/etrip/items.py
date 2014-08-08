# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EtripHotel(scrapy.Item):
    hotel_id = scrapy.Field()
    places = scrapy.Field()
    new_feed_place = scrapy.Field()
