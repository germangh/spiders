# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MomondoHotel(scrapy.Item):
    hotel_id = scrapy.Field()
    places = scrapy.Field()
    new_feed_place = scrapy.Field()
    description = scrapy.Field()
    nb_images = scrapy.Field()
    nb_reviews = scrapy.Field()
    hc_sentiment = scrapy.Field()
    rating_value = scrapy.Field()
