import random
import sh
import time


class RandomUserAgentMiddleware(object):

    def __init__(self):
        self.crawler = None

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        o.crawler = crawler
        return o

    def process_request(self, request, spider):
        ua = random.choice(self.crawler.settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):
    def __init__(self):
        self.crawler = None

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        o.crawler = crawler
        return o

    def process_request(self, request, spider):
        request.meta['proxy'] = self.crawler.settings.get('HTTP_PROXY')


class TorRetryMiddleware(object):

    def __init__(self, counter=0):
        self.crawler = None
        self.counter = counter

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        o.crawler = crawler
        return o

    def process_request(self, request, spider):
        self.counter += 1
        if self.counter > self.crawler.settings.getint('TOR_RENEW'):
            # Try renewing Tor's exit point and try again
            pidof = sh.pidof
            kill = sh.kill
            kill('-s', 'SIGHUP', pidof('tor').rstrip('\n'))
            time.sleep(self.crawler.settings.getint('TOR_WAIT'))
