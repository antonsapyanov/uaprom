from cache import RedisCache
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
                                      query=environ.get('QUERY_STRING'))

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
