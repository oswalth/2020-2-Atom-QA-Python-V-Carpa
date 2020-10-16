from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from ui.locators import basic_locators

RETRY_COUNT = 3


class BasePage(object):
    locators = basic_locators.BasePageLocators()

    def __init__(self, driver):
        self.driver = driver

    def check_if_exists(self, locator, value):
        by, locator = locator
        try:
            self.find((by, locator.format(value)), timeout=5)
            return True
        except TimeoutException:
            return False

    def find(self, locator, timeout=None) -> WebElement:
        # нотация WebElement удобна тем, что у метода find становятся доступны методы WebElement
        # а это очень удобно

        return self.wait(timeout).until(EC.presence_of_element_located(locator))  # поиск элемента с ожиданием

    def click(self, locator, timeout=None):
        # попытки чтобы кликнуть
        for i in range(RETRY_COUNT):
            try:
                element = self.find(locator, timeout) #self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return

            except StaleElementReferenceException:
                if i < RETRY_COUNT - 1:
                    pass
        raise

    def upload_file(self, locator, file_path, submit=None):
        upload_field = self.find(locator)
        upload_field.send_keys(file_path)
        if submit:
            self.click(locator=submit, timeout=4)

    def fill_field(self, locator, field_value):
        field = self.find(locator=locator)
        field.clear()
        field.send_keys(field_value)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)