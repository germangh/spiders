import scrapy
from momondo.items import MomondoHotel
import os.path
import csv

_ROOT_DIR = os.path.split(os.path.abspath(__file__))[0]
_BASE_URL = 'http://hotels.momondo.com/Hotel/'


class MomondoSpider(scrapy.Spider):
    name = 'momondo'
    allowed_domains = ['momondo.com']

    # We will crawl all hotels for which we have any description, i.e. hotels
    # that have not been crawled yet
    with open(os.path.join(_ROOT_DIR, 'hotel_url.csv'), 'r') as f:
        start_urls = [_BASE_URL + row[0] + '.htm' for row in csv.reader(f)]

    def parse(self, response):

        item = MomondoHotel()
        item['hotel_id'] = response.xpath(
            '//div[@class="hc_f_t_btn3 hc_f_submit"]').re(
                '(\d{5,})')
        if len(item['hotel_id']) < 1:
            item['hotel_id'] = None

        try:
            item['description'] = response.xpath(
                '//p[contains(@id, "hc_htl_desc")]').re(
                'HC.Hotel.formatHotelDescription\(.(.+).\)')[0]
        except IndexError:
            # Hotel has no description
            item['description'] = ''

        try:
            item['nb_images'] = len(response.xpath(
                '//span[contains(@id, "photoGallery")]').re(
                    'hc_thumb'))
        except:
            item['nb_images'] = 0

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
