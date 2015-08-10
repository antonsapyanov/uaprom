from flask import Flask

STORAGE = {}

app = Flask(__name__)


@app.route('/count/<key>')
def handle(key):
    STORAGE[key] = STORAGE.get(key, 0) + 1
    return str(STORAGE[key])


if __name__ == '__main__':
    app.run()
