from wsgiref.simple_server import make_server
from middleware import SessionMiddleware
from app import send_json_data

make_server('', 8000, SessionMiddleware(send_json_data)).serve_forever()
