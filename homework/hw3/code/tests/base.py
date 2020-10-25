import pytest
from _pytest.fixtures import FixtureRequest

from api.client import ApiClient
from conftest import Settings


class BaseCase:

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, config: Settings, request: FixtureRequest):
        self.config = config
        self.api_client: ApiClient = request.getfixturevalue('api_client')
