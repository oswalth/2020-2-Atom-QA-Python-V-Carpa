import pytest
import settings
from client.socket_client import SocketClient
from atom_app import flask_app
from mocks.mock_http_server import SimpleHttpServer
from settings import *


@pytest.fixture(scope="session")
def app_server():
    return flask_app.run_app(settings.APP_HOST, settings.APP_PORT)


@pytest.fixture(scope="session")
def mock_server():
    server = SimpleHttpServer(settings.MOCK_HOST, settings.MOCK_PORT)
    server.start()
    yield server
    server.stop()


@pytest.fixture(scope="function")
def socket_client():
    return SocketClient(settings.APP_HOST, settings.APP_PORT)
