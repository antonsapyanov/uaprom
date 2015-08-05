import asyncio


# @asyncio.coroutine
# def compute(x, y):
#     print("Compute %s + %s ..." % (x, y))
#     yield from asyncio.sleep(1.0)
#     return x + y
#
#
# @asyncio.coroutine
# def print_sum(x, y):
#     result = yield from compute(x, y)
#     print("%s + %s = %s" % (x, y, result))
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait([print_sum(1, 2), print_sum(4, 22), print_sum(131, 2)]))
# loop.close()

# @asyncio.coroutine
# def greet_always():
#     while True:
#         print("Hello, World!")
#         yield from asyncio.sleep(2)
#         yield from wait_additional_one_second()
#
# @asyncio.coroutine
# def wait_additional_one_second():
#     print("(additional second ...")
#     yield from asyncio.sleep(1)
#
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(greet_always())
# finally:
#     loop.close()


@asyncio.coroutine
def slow_operation(future):
    yield from asyncio.sleep(1)
    future.set_result('Future is done!')

loop = asyncio.get_event_loop()
future = asyncio.Future()
loop.create_task(slow_operation(future))
loop.run_until_complete(future)
print(future.result())
loop.close()