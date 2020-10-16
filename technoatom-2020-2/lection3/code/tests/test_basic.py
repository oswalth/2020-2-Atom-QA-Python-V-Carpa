import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.wait import WebDriverWait

from tests.base import BaseCase
from ui.locators import basic_locators


class Test(BaseCase):

    @pytest.mark.skip(reason='no need')
    def test_basic(self):
        assert 'Python' in self.driver.title

    @pytest.mark.skip(reason='no need')
    @pytest.mark.parametrize('query', ['pycon', 'python'])
    def test_search(self, query):
        self.base_page.search(query)
        assert "No results found." not in self.driver.page_source

    # @pytest.mark.skip(reason='no need')
    def test_search_negative(self):
        self.search_page.search('23132173152361253675216735126735132516736712')
        self.search_page.find(self.search_page.locators.NO_RESULTS).is_displayed()
    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)
    @pytest.mark.skip(reason='no need')
    def test_carousel(self):
        self.main_page.click(self.main_page.locators.COMPREHENSIONS, timeout=12)

    @pytest.mark.skip(reason='no need')
    def test_count(self):
        # негативный тест, ожидаем конкретный exception, а не любой, это важно
        # проверяем что количество элементов у нас 2 на странице
        with pytest.raises(TimeoutException):
            self.count_elements(basic_locators.NO_SUCH_ELEMENT, count=2)

    # @pytest.mark.skip(reason='no need')
    def test_euro_python(self):
        events = self.base_page.find(self.main_page.locators.EVENTS)

        ac = ActionChains(self.driver)
        ac.move_to_element(events).perform()

        with allure.step('Go to euro python page'):
            europython_page = self.main_page.go_to_europython_events()
        with allure.step('Click euro python events'):
            europython_page.click(europython_page.locators.EURO_PYTHON)

        assert 'Dublin' in self.driver.page_source

    @pytest.mark.skip(reason='no need')
    def test_page_changed(self):
        # псевдо тест, просто чтобы можно было проверить работу метода click
        # эмулируя попытки
        self.main_page.click(self.main_page.locators.GO_BUTTON)

    @pytest.mark.skip(reason='no need')
    def test_relative(self):
        intro = self.main_page.find(self.main_page.locators.INTRODUCTION)
        learn_more = intro.find_element(*self.main_page.locators.LEARN_MORE)

        if self.config['url'].startswith('https'):
            expected = self.config['url']
        else:
            expected = self.config['url'].replace('http', 'https')

        assert learn_more.get_attribute('href') == f'{expected}/doc/'

    @pytest.mark.skip(reason='no need')
    def test_options(self):
        self.driver.get('https://expired.badssl.com/')
        self.find((By.XPATH, '//*[@id="content"]/h1'))

    @pytest.mark.skip(reason='no need')
    def test_download(self):
        self.driver.get('https://www.python.org/downloads/release/python-382/')
        self.click((By.XPATH, '//*[contains(text(), "Windows x86-64 web-based installer")]'))

        self.wait_download('python-3.8.2-amd64-webinstall.exe')
