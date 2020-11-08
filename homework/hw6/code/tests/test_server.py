import json
import time
import pytest
from mocks.mock_http_server import SimpleHttpServer
from client.socket_client import SocketClient
import settings


class TestMock:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, app_server, socket_client):
        self.app = app_server
        yield time.sleep(3)

    @pytest.mark.API
    def test_mock_off(self, socket_client):
        response = socket_client.get_('/')
        assert response.get('msg') == f'TURNOFF_ERROR-{settings.MOCK_HOST}:{settings.MOCK_PORT}'


class TestServer:
    @pytest.fixture(scope="session", autouse=True)
    def setup(self, app_server, mock_server):
        self.app = app_server
        self.mock: SimpleHttpServer = mock_server
        self.mock.set_data({'alpha': ["first message"], 'betta': []})
        time.sleep(2)
        yield
        client = SocketClient(settings.APP_HOST, settings.APP_PORT)
        client.get_(params="/shutdown")

    @pytest.mark.API
    def test_mock_timeout(self, socket_client):
        with pytest.raises(TimeoutError):
            response = socket_client.get_('/timeout')

    @pytest.mark.API
    def test_server_500(self, socket_client):
        response = socket_client.get_('/server_error')
        assert response.get('msg') == f"SERVER_ERROR-{settings.MOCK_HOST}:{settings.MOCK_PORT}" and response.get(
            'code') == '500'

    @pytest.mark.POST
    def test_post_positive(self, socket_client):
        data = {"post": "second message"}
        response = socket_client.post_(params="/",
                                       data=json.dumps(data),
                                       headers=[("Host", "127.0.0.1"),
                                                ('Authorization', 'alpha'),
                                                ("Content-Type", "application/json")])
        code, message = response.get('code', '-1'), response.get('post')
        assert int(code) == 200 and message == data.get('post')

    @pytest.mark.POST
    def test_post_unauthorized(self, socket_client):
        data = {"post": "second message"}
        response = socket_client.post_(params="/",
                                       data=json.dumps(data),
                                       headers=[("Host", "127.0.0.1"),
                                                ("Content-Type", "application/json")])
        code, message = response.get('code', '-1'), response.get('msg')
        assert int(code) == 403 and message == "Unauthorized access"

    @pytest.mark.POST
    def test_post_user_not_found(self, socket_client):
        data = {"post": "second message"}
        response = socket_client.post_(params="/",
                                       data=json.dumps(data),
                                       headers=[("Host", "127.0.0.1"),
                                                ('Authorization', 'gamma'),
                                                ("Content-Type", "application/json")])
        code, message = response.get('code', '-1'), response.get('msg')
        assert int(code) == 400 and message == "User not found"

    @pytest.mark.POST
    def test_post_incorrect_request_body(self, socket_client):
        data = '{"post": "second message}'
        response = socket_client.post_(params="/",
                                       data=data,
                                       headers=[("Host", "127.0.0.1"),
                                                ('Authorization', 'alpha'),
                                                ("Content-Type", "application/json")])
        code, message = response.get('code', '-1'), response.get('msg')
        assert int(code) == 400 and message == "Incorrect request body"

    @pytest.mark.PUT
    def test_put_positive(self, socket_client):
        data = {"post": "first message", "edited": "last message"}
        response = socket_client.put_(params="/",
                                       data=json.dumps(data),
                                       headers=[("Host", "127.0.0.1"),
                                                ('Authorization', 'alpha'),
                                                ("Content-Type", "application/json")])
        code, message = response.get('code', '-1'), response.get('post')
        assert int(code) == 200 and message == data.get('edited')

    @pytest.mark.PUT
    def test_put_unauthorized(self, socket_client):
        data = {"post": "first message", "edited": "last message"}
        response = socket_client.put_(params="/",
                                       data=json.dumps(data),
                                       headers=[("Host", "127.0.0.1"),
                                                ("Content-Type", "application/json")])
        code, message = response.get('code', '-1'), response.get('msg')
        assert int(code) == 403 and message == "Unauthorized access"

    @pytest.mark.PUT
    def test_put_user_not_found(self, socket_client):
        data = {"post": "first message", "edited": "last message"}
        response = socket_client.put_(params="/",
                                       data=json.dumps(data),
                                       headers=[("Host", "127.0.0.1"),
                                                ('Authorization', 'gamma'),
                                                ("Content-Type", "application/json")])
        code, message = response.get('code', '-1'), response.get('msg')
        assert int(code) == 400 and message == "User not found"

    @pytest.mark.PUT
    def test_put_incorrect_request_body(self, socket_client):
        data = '{"post": "first message", "edited": "last message}'
        response = socket_client.put_(params="/",
                                       data=data,
                                       headers=[("Host", "127.0.0.1"),
                                                ('Authorization', 'alpha'),
                                                ("Content-Type", "application/json")])
        code, message = response.get('code', '-1'), response.get('msg')
        assert int(code) == 400 and message == "Incorrect request body"

    @pytest.mark.PUT
    def test_put_post_not_found(self, socket_client):
        data = {"post": "non-exist message", "edited": "last message"}
        response = socket_client.put_(params="/",
                                      data=json.dumps(data),
                                      headers=[("Host", "127.0.0.1"),
                                               ('Authorization', 'alpha'),
                                               ("Content-Type", "application/json")])
        code, message = response.get('code', '-1'), response.get('msg')
        assert int(code) == 400 and message == "Post was not found"
