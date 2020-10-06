from ui.locators import basic_locators
from ui.pages.base_page import BasePage
from ui.pages.euro_python_events_page import EuroPythonEventsPage


class MainPage(BasePage):
    locators = basic_locators.MainPageLocators()

    def go_to_europython_events(self):
        self.click(self.locators.PYTHON_EVENTS)
        return EuroPythonEventsPage(self.driver)
