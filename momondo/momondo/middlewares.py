import random


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
