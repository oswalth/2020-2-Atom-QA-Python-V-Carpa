from selenium.common.exceptions import TimeoutException

from ui.locators import basic_locators
from ui.pages.base_page import BasePage


class AudiencePage(BasePage):
    locators = basic_locators.AudiencePageLocators()

    def get_segment_id(self, locator, value):
        by, locator = locator
        element = self.find((by, locator.format(value)))
        return element.get_attribute('href').split('/')[-1]

    def create_segment(self, segment_name):
        try:
            self.find(self.locators.SEGMENT_DISPLAY_NONE)
            self.click(self.locators.CREATE_SEGMENT_LINK)

        except TimeoutException:
            self.click(self.locators.CREATE_SEGMENT_BUTTON)
        self.click(self.locators.APP_GAMES_LOCATOR)
        self.click(self.locators.SEGMENT_INPUT_CHECKBOX)
        self.click(self.locators.ADD_SEGMENT_BUTTON, timeout=2)
        self.fill_field(self.locators.SEGMENT_NAME_INPUT, segment_name)
        self.click(self.locators.CREATE_SEGMENT_FINAL_BUTTON)

    def delete_segment(self, segment_name):
        segment_id = self.get_segment_id(self.locators.SEGMENT_NAME_LOCATOR, segment_name)
        by, delete_locator = self.locators.SEGMENT_DELETE_BTN
        self.click((by, delete_locator.format(segment_id)))
        self.click(self.locators.SEGMENT_DELETE_CONFIRM)