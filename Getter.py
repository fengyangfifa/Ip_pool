from ip_pool.crawl import Crawler
from ip_pool.storage import RedisClient
from ip_pool.setting import *


class Getter:
    def __init__(self):
        self.redis = RedisClient()
        self.crawl = Crawler()

    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        if not self.is_over_threshold():
            for callback_label in range(self.crawl.__CrawlFuncCount__):
                callback = self.crawl.__CrawlFunc__[callback_label]
                proxies = self.crawl.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
