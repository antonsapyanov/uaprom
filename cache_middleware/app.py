from wsgiref.simple_server import make_server
from middleware import CacheMiddleware
from views import router

make_server('', 8000, CacheMiddleware(router)).serve_forever()
