import scrapy
from etrip.items import EtripHotel
import os.path
import csv

_ROOT_DIR = os.path.split(os.path.abspath(__file__))[0]
_BASE_URL = 'http://hotels.etrip.net/Hotel/'


class EtripSpider(scrapy.Spider):
    name = 'etrip'
    allowed_domains = ['etrip.net']

    with open(os.path.join(_ROOT_DIR, 'hotel_url.csv'), 'r') as f:
        start_urls = [_BASE_URL + row[0] + '.htm' for row in csv.reader(f)]

    def parse(self, response):

        item = EtripHotel()
        item['hotel_id'] = response.xpath(
            '//a[contains(@href, "javascript:void(0);")]/@onclick').re(
                '(\d{5,})')
        item['places'] = response.xpath(
            '//div[contains(@id, "hc_bc")]/ul/li/a/@href').re(
            'Place/(.+)\.htm')
        item['new_feed_place'] = response.xpath(
            '//script[contains(@type, "text/javascript")]').re(
            'place:\s*([\w_]+)')[0]

        try:
            item['description'] = response.xpath(
                '//script[contains(@type, "text/javascript")]').re(
                'HC.Hotel.formatHotelDescription\(.(.+).\)')[0]
        except IndexError:
            # Empty description is not the sames a "missing value". The latter
            # are to indicate that we have not crawled that hotel yet.
            item['description'] = ''

        try:
            item['nb_images'] = len(response.xpath(
                '//span[contains(@id, "photoGallery")]').re(
                    'hc_thumb'))
        except:
            item['nb_images'] = None

        try:
            item['nb_reviews'] = response.xpath(
                '//div[contains(@class, "hc_htl_usrRating_numReviews")]/'
                '@content').extract()
        except:
            item['nb_reviews'] = None

        try:
            item['hc_sentiment'] = response.xpath(
                '//div[@class="hc_sentiment"]/text()').extract()
        except:
            item['hc_sensiment'] = None

        try:
            item['rating_value'] = response.xpath(
                '//span[contains(@id, "ReviewRatingTagLine")]/'
                '@content').extract()[0]
        except:
            item['rating_value'] = None

        return item
