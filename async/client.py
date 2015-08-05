import asyncio
import sys


END = b': Bye-bye!\n'
argv = bytes(str(sys.argv[1]).encode())

@asyncio.coroutine
def echo_client():
    reader, writer = yield from asyncio.open_connection('localhost', 8000)
    print(argv + b': Hello, World!\n')
    writer.write(argv + b': Hello, World!\n')
    print(argv + b': This is a fine day!\n')
    writer.write(argv + b': This is a fine day!\n')
    print(argv + END)
    writer.write(argv + END)
    while True:
        line = yield from reader.readline()
        print("received back: ", line)
        if line == argv + END or not line:
            break
    writer.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(echo_client())
