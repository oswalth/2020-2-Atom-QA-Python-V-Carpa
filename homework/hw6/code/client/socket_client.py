import json
import socket
from json.decoder import JSONDecodeError


class SocketClient:
    def __init__(self, host, port, timeout=2):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(timeout)

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
        except ConnectionRefusedError:
            return {'msg': f'TURNOFF_ERROR-{self.host}:{self.port}', 'code': 500}

    def get_response(self):
        total_data = []
        while True:
            try:
                data = self.client.recv(4096)
                if data:
                    total_data.append(data.decode())
                else:
                    break
            except socket.timeout:
                self.client.close()
                raise TimeoutError(f"Timeout exceeded {self.timeout}s")

        lines = ''.join(total_data).splitlines()
        code = lines[0].split()[1]

        try:
            response = json.loads(lines[-1])
            response['code'] = code
        except JSONDecodeError:
            if code == '500':
                response = {'msg': f'SERVER_ERROR-{self.host}:{self.port}', 'code': code}
            elif code in ['400', '403']:
                response = {'msg': lines[-1], 'code': code}
            else:
                response = {'msg': 'DECODE_ERROR', 'code': code}
        self.client.close()
        return response

    def get_(self, params='/'):
        connect_error = self.connect()
        if connect_error:
            return connect_error
        request = f"GET {params} HTTP/1.1\r\nAuthorization: True\r\nContent-Type: application/json\r\n\r\n"
        self.client.send(request.encode())
        return self.get_response()

    def post_(self, params, data, headers):
        connect_error = self.connect()
        if connect_error:
            return connect_error
        str_headers = "\r\n".join([f"{header[0]}: {header[1]}" for header in headers])
        header = (f""
                  f"POST {params} HTTP/1.1\r\n"
                  f"{str_headers}\r\n"
                  f"Content-Length: {str(len(data))}\r\n\r\n{data}")

        self.client.send(header.encode())
        return self.get_response()

    def put_(self, params, data, headers):
        connect_error = self.connect()
        if connect_error:
            return connect_error
        str_headers = "\r\n".join([f"{header[0]}: {header[1]}" for header in headers])
        request = (f""
                   f"PUT {params} HTTP/1.1\r\n"
                   f"{str_headers}\r\n"
                   f"Content-Length: {str(len(data))}\r\n\r\n{data}")

        self.client.send(request.encode())
        return self.get_response()
