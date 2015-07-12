def send_json_data(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'application/json')]
    encoding = 'utf-8'
    start_response(status, headers)

    return [open('data', 'r', encoding=encoding).read()]
