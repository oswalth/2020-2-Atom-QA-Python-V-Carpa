import pytest
from api.client import ApiClient
from dataclasses import dataclass


@dataclass
class Settings:
    email: str = None
    password: str = None


@pytest.fixture(scope='function')
def config(request) -> Settings:
    settings = Settings()
    settings.email = 'oswalth3@gmail.com'
    settings.password = 'cpu#N7ZvD6'

    return settings


@pytest.fixture(scope='function')
def api_client(config):
    client = ApiClient(config)
    yield client
    client.session.close()
