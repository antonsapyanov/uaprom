import asyncio


@asyncio.coroutine
def echo_server():
    print("Create connection ...")
    yield from asyncio.start_server(handle_connection, 'localhost', 8000)


@asyncio.coroutine
def handle_connection(reader, writer):
    while True:
        print("Receiving the data ...")
        yield from asyncio.sleep(3)
        data = yield from reader.readline()
        if not data:
            print("no data")
            break
        print('received: ', data)
        writer.write(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(echo_server())
loop.run_forever()
