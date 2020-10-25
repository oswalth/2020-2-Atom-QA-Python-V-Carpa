from dataclasses import dataclass

import pytest

from api.client import ApiClient


@dataclass
class Settings:
    URL: str = None


@pytest.fixture(scope='function')
def config(request) -> Settings:
    settings = Settings()
    settings.URL = 'https://jsonplaceholder.typicode.com/'

    return settings

@pytest.fixture(scope='function')
def api_client(config):
    return ApiClient(config)