import asyncio
from aiohttp import web

STORAGE = {}


@asyncio.coroutine
def handle(request):
    key = request.match_info.get('key')
    STORAGE[key] = STORAGE.get(key, 0) + 1
    body = str(STORAGE[key])
    return web.Response(body=body.encode('utf-8'))


@asyncio.coroutine
def deferred_handle(request):
    key = request.match_info.get('key')
    STORAGE[key] = STORAGE.get(key, 0) + 1
    body = str(STORAGE[key])

    yield from asyncio.sleep(0.5)

    return web.Response(body=body.encode('utf-8'))


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
    app.router.add_route('GET', '/count/{key}', deferred_handle)
    app.router.add_route('GET', '/fibonacci/{index}', fibonacci)

    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 8080)
    print("Server started at http://127.0.0.1:8080")
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
