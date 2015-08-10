from flask import Flask

STORAGE = {}

app = Flask(__name__)


@app.route('/count/<key>')
def handle(key):
    STORAGE[key] = STORAGE.get(key, 0) + 1
    return str(STORAGE[key])


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
