import os

import redis


class FileCache(object):
    DEFAULT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cache')

    def __init__(self, **kwargs):
        self.path = kwargs.get('path', self.DEFAULT_PATH)

    def __getitem__(self, url):
        given_h_url = str(hash(url))
        fd = os.open(self.path, os.O_RDONLY | os.O_CREAT)
        with os.fdopen(fd) as file:
            for line in file:
                got_h_url, response = self._parse_line(line)
                if given_h_url == got_h_url:
                    return response.encode()

    def __setitem__(self, url, response):
        given_h_url = hash(url)
        fd = os.open(self.path, os.O_RDWR)
        with os.fdopen(fd, 'a+') as file:
            line = "{0}:{1}\n".format(given_h_url, response)
            file.write(line)

    def __contains__(self, url):
        given_h_url = str(hash(url))
        fd = os.open(self.path, os.O_RDONLY | os.O_CREAT)
        with os.fdopen(fd) as file:
            for line in file:
                got_h_url, response = self._parse_line(line)
                if given_h_url == got_h_url:
                    return True
            return False

    @staticmethod
    def _parse_line(line):
        return line.strip().split(':')


class RedisCache(object):
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 6379

    def __init__(self, **kwargs):
        host = kwargs.get('host', self.DEFAULT_HOST)
        port = kwargs.get('port', self.DEFAULT_PORT)
        self.server = redis.StrictRedis(host, port)

    def __getitem__(self, url):
        return self.server.get(url)

    def __setitem__(self, url, response):
        self.server.set(url, response)

    def __contains__(self, url):
        return self.server.exists(url)


class MemoryCache(object):
    def __init__(self, **kwargs):
        pass

    def __getitem__(self, url):
        pass

    def __setitem__(self, url, response):
        pass

    def __contains__(self, url):
        pass
