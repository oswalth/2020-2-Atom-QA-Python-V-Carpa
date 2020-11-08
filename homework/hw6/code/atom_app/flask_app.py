import threading
import settings
from flask import Flask, jsonify, request, make_response
from client.socket_client import SocketClient


app = Flask(__name__)
DATA = {}


def run_app(host, port):
    server = threading.Thread(target=app.run, kwargs={
        "host": host,
        "port": port,
    })
    server.start()
    return server


def shutdown_app():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_app()
    return make_response(jsonify({"msg": "SERVER_SHUTDOWN"}))


@app.route('/', methods=['GET', 'POST', 'PUT'])
def index():
    client = SocketClient(host=settings.MOCK_HOST, port=settings.MOCK_PORT)
    if request.method == 'GET':
        response = client.get_(params='/')
        code = response.get('code', 500)
    elif request.method == 'POST':
        response = client.post_(params='/', data=request.data.decode(), headers=list(dict(request.headers).items()))
        code = response.get('code', 500)
    elif request.method == 'PUT':
        response = client.put_(params='/', data=request.data.decode(), headers=list(dict(request.headers).items()))
        code = response.get('code', 500)
    return make_response(jsonify(response), code)


@app.route('/timeout')
def fast_request():
    client = SocketClient(host=settings.MOCK_HOST, port=settings.MOCK_PORT)
    response = client.get_(params='/timeout')
    code = response.get('code', 500)
    return make_response(jsonify(response), code)


@app.route('/server_error')
def server_error():
    client = SocketClient(host=settings.MOCK_HOST, port=settings.MOCK_PORT)
    response = client.get_(params='/server_error')
    return make_response(jsonify(response), 500)


if __name__ == '__main__':
    run_app(settings.APP_HOST, settings.APP_PORT)
