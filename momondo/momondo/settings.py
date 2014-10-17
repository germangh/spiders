# -*- coding: utf-8 -*-

# Scrapy settings for etrip project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os.path
import yaml

ROOT_DIR = os.path.split(os.path.abspath(__file__))[0]

BOT_NAME = 'momondo'

SPIDER_MODULES = ['momondo.spiders']
NEWSPIDER_MODULE = 'momondo.spiders'

# Some site use cookies to detect bots
COOKIES_ENABLED = False

# Avoid hitting momondo too hard by having a delay between consecutive requests
DOWNLOAD_DELAY = 5

# Automatically renew TOR IP after TOR_RENEW requests. Wait for TOR_WAIT
# seconds for the renewal to take place
TOR_RENEW = 40
TOR_WAIT = 10     # in seconds

# The user agent will be changed from a pool of valid user agents, this is just
# the default user agent

f = open(os.path.join(ROOT_DIR, 'user_agents.yaml'), 'r')
USER_AGENT_LIST = yaml.load(f)

# polipo HTTP server, which redirects to the Tor network
HTTP_PROXY = 'http://127.0.0.1:8123'

DOWNLOADER_MIDDLEWARES = {
    # Now we just run a cron job renewing the IP every now and then
    'momondo.middlewares.TorRenewMiddleware': 390,
    'momondo.middlewares.RandomUserAgentMiddleware': 400,
    'momondo.middlewares.ProxyMiddleware': 410,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware':
        None
    # Disable compression middleware, so the actual HTML pages are cached
    # Important to disable the scrapy UserAgentMiddleware above. Otherwise you
    # will be detected as a scapy spider!
}
