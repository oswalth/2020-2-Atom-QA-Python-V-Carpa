from selenium.webdriver.common.by import By


class BasePageLocators:
    QUERY_LOCATOR = (By.NAME, 'q')
    GO_BUTTON = (By.ID, 'submit')


class MainPageLocators(BasePageLocators):
    COMPREHENSIONS = (By.XPATH, '//span[@class="comment" and contains(text(), "comprehensions")]')
    EVENTS = (By.XPATH, '//nav[@id="mainnav"]//a[@href="/events/" and contains(text(), "Events")]')
    PYTHON_EVENTS = (By.XPATH, '//li[@id="events"]//a[@href="/events/python-events"]')
    INTRODUCTION = (By.CLASS_NAME, 'introduction')
    LEARN_MORE = (By.CLASS_NAME, 'readmore')


class SearchPageLocators(BasePageLocators):
    QUERY_LOCATOR = (By.NAME, 'q')
    NO_RESULTS = (By.XPATH, '//p[contains(text(), "No results found.")]')
    NO_SUCH_ELEMENT = (By.NAME, '2132132131231231231231231')


class EuroPythonEventsPageLocators(BasePageLocators):
    EURO_PYTHON = (By.XPATH, '//a[@href="/events/python-events/964/"]')
