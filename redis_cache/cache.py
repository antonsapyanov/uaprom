import redis


DEFAULT_EXPIRE = 5  # 5 seconds (in seconds)


class RedisCache(object):
    def __init__(self, host, port):
        self.server = redis.StrictRedis(host, port)

    def __contains__(self, url):
        return self.server.exists(url)

    def __getitem__(self, url):
        return self.server.get(url)

    def __setitem__(self, url, value):
        response = value.response
        expire = value.expire

        if expire is None:
            expire = DEFAULT_EXPIRE

        self.server.set(url, response)
        self.server.expire(url, expire)
