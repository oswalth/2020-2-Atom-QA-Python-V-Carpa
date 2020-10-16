import os

import pytest
from _pytest.fixtures import FixtureRequest
from ui.decorators import wait
from ui.pages.base_page import BasePage
from ui.pages.euro_python_events_page import EuroPythonEventsPage
from ui.pages.main_page import MainPage
from ui.pages.search_page import SearchPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.search_page: SearchPage = request.getfixturevalue('search_page')
        self.euro_python_events_page: EuroPythonEventsPage = request.getfixturevalue('euro_python_events_page')

    def wait_download(self, file_name, timeout=30):

        def _check_download(_):
            for f in os.listdir(self.config['download_dir']):
                if f.endswith('.crdownload'):
                    return False

            if file_name in os.listdir(self.config['download_dir']):
                return True

            return False

        wait(method=_check_download, timeout=timeout)

Каким способом можно сделать фикстуру, в которую можно передавать аргументы? Например фикстура для авторизации