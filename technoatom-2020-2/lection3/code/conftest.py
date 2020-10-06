import pytest as pytest
from ui.fixtures import *

def pytest_addoption(parser):
    parser.addoption('--url', default='http://www.python.org')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--browser_ver', default='latest')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')

    return {'browser': browser, 'version': version, 'url': url, 'download_dir': '/tmp'}
