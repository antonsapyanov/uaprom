import asyncio
import aiohttp

from aiohttp import web
from .config import config


@asyncio.coroutine
def handle(request):
    key = request.match_info.get('key')
    response = yield from aiohttp.get("http://{host}:{port}/count/{key}".format(host=config['MAIN_ASYNC_SERVER_HOST'],
                                                                                port=config['MAIN_ASYNC_SERVER_PORT'],
                                                                                key=key))
    text = yield from response.text()

    return web.Response(body=text.encode('utf-8'))


@asyncio.coroutine
def fibonacci(request):
    index = int(request.match_info.get('index'))
    a = b = 1
    for _ in range(index - 1):
        tmp = a
        a = b
        b += tmp
    return web.Response(body=str(a).encode('utf-8'))


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/count/{key}', handle)
    app.router.add_route('GET', '/fibonacci/{index}', fibonacci)

    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 7777)
    print("Server started at http://127.0.0.1:7777")
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
