def send_json_data(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'application/json')]

    start_response(status, headers)
    return [str(__import__('random').randint(0, 100)).encode()]
    # return [open('data', 'r').read().encode()]
