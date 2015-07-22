import redis
import json


# DEFAULT_EXPIRE = 60 * 60 * 24 * 1  # 1 day (in seconds)
DEFAULT_EXPIRE = 5  # 5 seconds (in seconds)


class RedisCache(object):
    def __init__(self, host, port):
        self.server = redis.StrictRedis(host, port)

    def exists(self, url):
        return self.server.exists(url)

    def get(self, url):
        return self.server.get(url)

    def set(self, url, response, expire=None):
        if expire is None:
            expire = DEFAULT_EXPIRE

        self.server.set(url, response)
        self.server.expire(url, expire)
