from cache import RedisCache
from urllib.parse import parse_qsl
import config


class SessionMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        cache = RedisCache(config.REDIS_HOST, config.REDIS_PORT)
        cache_control = do_caching(environ.get('Cache-Control', ''))
        url = "{path}?{query}".format(path=environ.get('PATH_INFO'),
                                      query=get_sorted_query(environ.get('QUERY_STRING')))

        if cache.exists(url):
            response = [cache.get(url)]
            start_response("200 OK", [('Content-Type', 'application/json')])
            return response
        else:
            response = self.app(environ, start_response)
            if cache_control:
                cache.set(url, "".join((piece.decode() for piece in response)))
            return response


def get_sorted_query(query_string):
    query_list = parse_qsl(query_string)
    query_list.sort(key=lambda value: value[0])
    return '&'.join(('='.join(pair) for pair in query_list))


def do_caching(header_value):
    return False if header_value == 'no-cache' else True
