from cache import RedisCache
from urllib.parse import parse_qsl
import config


class SessionMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def wrapped_start_response(resp_status, resp_headers):
            status_and_headers['status'] = resp_status
            status_and_headers['headers'] = resp_headers
            return start_response(resp_status, resp_headers)

        cache = RedisCache(config.REDIS_HOST, config.REDIS_PORT)
        url = "{path}?{query}".format(path=environ.get('PATH_INFO'),
                                      query=get_sorted_query(environ.get('QUERY_STRING')))

        if cache.exists(url):
            status, headers, response = cache.get(url)
            start_response(status, headers)
            return response
        else:
            status_and_headers = {}
            response = self.app(environ, wrapped_start_response)
            status = status_and_headers['status']
            headers = status_and_headers['headers']
            cache.set(url, status, headers, response)
            return response


def get_sorted_query(query_string):
    query_list = parse_qsl(query_string)
    query_list.sort(key=lambda value: value[0])
    return '&'.join('='.join(pair) for pair in query_list)
