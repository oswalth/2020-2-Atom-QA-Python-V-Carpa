import time

import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from ui.pages.account_page import AccountPage
from ui.pages.audience_page import AudiencePage
from ui.pages.base_page import BasePage
from ui.pages.campaign_page import CampaignPage
from ui.pages.main_page import MainPage


class UnsupportedBrowserException(Exception):
    pass


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture
def account_page(driver):
    def authorize(email, password):
        page = MainPage(driver=driver)
        page.click(page.locators.LOGIN_BUTTON, timeout=5)
        page.fill_field(page.locators.EMAIL_INPUT, email)
        page.fill_field(page.locators.PASSWORD_INPUT, password)
        page.click(page.locators.CONFIRM_LOGIN_BUTTON, timeout=5)
        return AccountPage(driver=driver)
    return authorize


@pytest.fixture
def campaign_page(driver):
    def _campaign(account_page):
        account_page.click(account_page.locators.HEADER_CAMPAIGN_BUTTON)
        return CampaignPage(driver=driver)
    return _campaign


@pytest.fixture
def audience_page(driver):
    def _audience(account_page):
        account_page.click(account_page.locators.HEADER_AUDIENCE_BUTTON)
        return AudiencePage(driver=driver)
    return _audience


@pytest.fixture(scope="function")
def driver(config):
    browser = config['browser']
    version = config['version']
    url = config['url']
    download_dir = config['download_dir']
    selenoid = config['selenoid']
    print(selenoid)
    if browser == 'chrome':
        options = ChromeOptions()
        if selenoid:
            capabilities = {'acceptInsecureCerts': True,
                            'browserName': 'chrome'
                            }

            driver = webdriver.Remote(command_executor=selenoid,
                                      options=options,
                                      desired_capabilities=capabilities
                                      )
        else:
            options.add_argument("--window-size=800,600")

            prefs = {"download.default_directory": download_dir}
            options.add_experimental_option('prefs', prefs)

            manager = ChromeDriverManager(version=version)
            driver = webdriver.Chrome(executable_path=manager.install(),
                                      options=options,
                                      desired_capabilities={'acceptInsecureCerts': True}
                                      )
    else:
        raise UnsupportedBrowserException(f'Unsupported browser: "{browser}"')

    driver.get(url)
    driver.maximize_window()
    yield driver

    # quit = закрыть страницу, остановить browser driver
    # close = закрыть страницу, бинарь browser driver останется запущенным
    driver.quit()