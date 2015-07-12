import redis
import json


DEFAULT_EXPIRE = 60 * 60 * 24 * 14  # 14 days (in seconds)

STATUS = b'status'
HEADERS = b'headers'
RESPONSE = b'response'


class RedisCache(object):
    def __init__(self, host, port):
        self.server = redis.StrictRedis(host, port)

    def exists(self, url):
        return self.server.exists(url)

    def get(self, url, mode='utf-8'):
        result = self.server.hgetall(url)

        status = result[STATUS].decode(mode)
        headers = [(key, value) for key, value in json.loads(str(result[HEADERS], mode)).items()]
        response = result[RESPONSE]

        return status, headers, [response]

    def set(self, url, status, headers, response, expire=None, encoding='utf-8'):
        if expire is None:
            expire = DEFAULT_EXPIRE

        status_bytes = status.encode(encoding)
        headers_bytes = json.dumps({key: value for key, value in headers}).encode(encoding)
        response_bytes = "".join(response)

        mapping = {
            STATUS: status_bytes,
            HEADERS: headers_bytes,
            RESPONSE: response_bytes
        }

        self.server.hmset(url, mapping)
        self.server.expire(url, expire)
