import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import JSONDecodeError


class MockHandlerRequests(BaseHTTPRequestHandler):
    data = None

    def _set_response(self, code):
        self.send_response(code)
        self.send_header("Content-type", 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/timeout':
            time.sleep(2)
            self._set_response(504)
        elif self.path == '/server_error':
            self._set_response(500)
        else:
            self._set_response(200)
            self.wfile.write(json.dumps({'msg': 'success get'}).encode())

    def do_POST(self):
        headers = dict(self.headers._headers)
        if 'Authorization' not in headers:
            code = 403
            message = "Unauthorized access"
        else:
            if headers['Authorization'] in self.data:
                content_length = int(self.headers['Content-Length'])
                if headers.get('Content-Type', None) == 'application/json':
                    try:
                        data = json.loads(self.rfile.read(content_length).decode())
                        self.data[headers['Authorization']].append(data.get('post'))
                        code = 200
                        message = json.dumps({"post": data.get('post')})
                    except JSONDecodeError:
                        code = 400
                        message = "Incorrect request body"
                else:
                    raise NotImplementedError
            else:
                code = 400
                message = "User not found"
        self._set_response(code)
        self.wfile.write(message.encode())

    def do_PUT(self):
        headers = dict(self.headers._headers)
        if 'Authorization' not in headers:
            code = 403
            message = "Unauthorized access"
        else:
            if headers['Authorization'] in self.data:
                content_length = int(self.headers['Content-Length'])
                if headers.get('Content-Type', None) == 'application/json':
                    try:
                        data = json.loads(self.rfile.read(content_length).decode())
                        try:
                            position = self.data[headers['Authorization']].index(data.get('post'))
                            self.data[headers['Authorization']][position] = data.get('edited')
                            code = 200
                            message = json.dumps({"post": data.get('edited')})
                        except ValueError:
                            code = 400
                            message = "Post was not found"
                    except JSONDecodeError:
                        code = 400
                        message = "Incorrect request body"
                else:
                    raise NotImplementedError
            else:
                code = 400
                message = "User not found"

        self._set_response(code)
        self.wfile.write(message.encode())


class SimpleHttpServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stop_server = False
        self.handler = MockHandlerRequests
        self.handler.data = None
        self.server = HTTPServer((self.host, self.port), self.handler)

    def start(self):
        self.server.allow_reuse_address = True
        th = threading.Thread(target=self.server.serve_forever)
        th.start()
        return self.server

    def stop(self):
        self.server.server_close()
        self.server.shutdown()

    def set_data(self, data):
        self.handler.data = data


if __name__ == '__main__':
    server = SimpleHttpServer('127.0.0.1', 1052)
    server.set_data({'vova': ["first message"], 'max': []})
    server.start()
