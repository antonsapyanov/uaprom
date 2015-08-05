from urllib.parse import parse_qsl
from config import cache_config
from cache import Cache


class CacheMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        cache = Cache(cache_config)
        cache_control = do_caching(environ.get('Cache-Control', ''))
        url = "{path}?{query}".format(path=environ.get('PATH_INFO'),
                                      query=get_sorted_query(environ.get('QUERY_STRING')))

        if url in cache:
            response = [cache[url]]
            start_response("200 OK", [('Content-Type', 'text/plain')])
        else:
            response = self.app(environ, start_response)
            if cache_control:
                cache[url] = "".join(piece.decode() for piece in response)
        return response


def get_sorted_query(query_string):
    query_list = parse_qsl(query_string)
    query_list.sort(key=lambda value: value[0])
    return '&'.join(('='.join(pair) for pair in query_list))


def do_caching(header_value):
    return False if header_value == 'no-cache' else True
