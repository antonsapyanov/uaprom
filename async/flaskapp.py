from flask import Flask
import requests
from .config import config

app = Flask(__name__)


@app.route('/count/<key>')
def handle(key):
    response = requests.get("http://{host}:{port}/count/{key}".format(host=config['MAIN_ASYNC_SERVER_HOST'],
                                                                      port=config['MAIN_ASYNC_SERVER_PORT'],
                                                                      key=key))
    return response.text


@app.route('/fibonacci/<int:index>')
def fibonacci(index):
    a = b = 1
    for _ in range(index - 1):
        tmp = a
        a = b
        b += tmp
    return str(a)

if __name__ == '__main__':
    app.run()
