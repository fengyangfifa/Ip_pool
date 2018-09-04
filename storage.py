import redis
from random import choice
from ip_pool.error import PoolEmptyError
from ip_pool.setting import *


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """添加代理"""
        if not self.db.zscore(REDIS_KEY, proxy):
            self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """随机返回一个代理"""
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """代理的score减1"""
        score = self.db.zscore(REDIS_KEY, proxy)
        if score > MIN_SCORE+1:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """判断代理是否存在"""
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def max(self, proxy):
        """设置代理的score为100"""
        print('代理', proxy, '可用, 设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """返回所有代理数量"""
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """返回所有代理"""
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """返回指定位置的代理"""
        return self.db.zrevrange(REDIS_KEY, start, stop-1)
