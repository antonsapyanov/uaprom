def send_json_data(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'application/json')]

    start_response(status, headers)
    return [open('data', 'r').read().encode()]
