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
            '//script[contains(@type, "text/javascript")]').re(
            'CurrentHotelID:\s*(\d+)')
        item['places'] = response.xpath(
            '//div[contains(@id, "hc_bc")]/ul/li/a/@href').re(
            'Place/(.+)\.htm')
        item['new_feed_place'] = response.xpath(
            '//script[contains(@type, "text/javascript")]').re(
            'place:\s*([\w_]+)')[0]
        return item
