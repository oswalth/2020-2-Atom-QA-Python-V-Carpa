import time

from ui.locators import basic_locators
from selenium.webdriver import ActionChains
from ui.pages.base_page import BasePage


class CampaignPage(BasePage):
    locators = basic_locators.CampaignPageLocators()

    def create_campaign(self, campaign_url, campaign_name, campaign_file):
        self.click(self.locators.CREATE_CAMPAIGN_BUTTON, timeout=3)
        self.click(self.locators.TRAFFIC_LOCATOR)
        self.fill_field(self.locators.URL_INPUT, campaign_url)
        self.click(self.locators.BANNER_ADS)
        self.upload_file(self.locators.IMG_INPUT, campaign_file, self.locators.SUBMIT_IMG)
        self.fill_field(self.locators.CAMPAIGN_NAME_INPUT, campaign_name)
        ac = ActionChains(self.driver)
        ac.move_to_element(self.find(self.locators.SUBMIT_CREATION)).perform()
        self.click(self.locators.SUBMIT_CREATION, timeout=10)
