from wsgiref.simple_server import make_server
from middleware import CacheMiddleware
from app import send_json_data

make_server('', 8000, CacheMiddleware(send_json_data)).serve_forever()
