import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.account_page import AccountPage
from ui.pages.audience_page import AudiencePage
from ui.pages.base_page import BasePage
from ui.pages.campaign_page import CampaignPage
from ui.pages.main_page import MainPage


class BaseCase:

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')


class CampaignSegmentCase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.account_page: AccountPage = request.getfixturevalue('account_page')(email="oswalth3@gmail.com", password="cpu#N7ZvD6")
