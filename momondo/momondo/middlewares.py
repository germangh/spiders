import random
from scrapy.exceptions import NotConfigured
from scrapy import log
from scrapy.utils.response import response_status_message
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

    def __init__(self, settings):
        if not settings.getbool('RETRY_ENABLED'):
            raise NotConfigured
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.retry_wait = settings.getint('RETRY_WAIT')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        if response.status != 200:
            # Try renewing Tor's exit point and try again
            from nose.tools import set_trace; set_trace()  # XXX BREAKPOINT
            pidof = sh.pidof
            kill = sh.kill
            kill('-s', 'SIGHUP', pidof('tor').rstrip('\n'))
            time.sleep(self.retry_wait)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        return response

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        if retries <= self.max_retry_times:
            log.msg(format="Retrying %(request)s (failed %(retries)d times):"
                    "%(reason)s", level=log.DEBUG, spider=spider,
                    request=request, retries=retries, reason=reason)
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            return retryreq
        else:
            log.msg(format="Gave up retrying %(request)s (failed"
                    "%(retries)d times): %(reason)s", level=log.DEBUG,
                    spider=spider, request=request, retries=retries,
                    reason=reason)
