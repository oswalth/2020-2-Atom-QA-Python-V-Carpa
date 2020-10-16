import pytest

from pathlib import Path, PureWindowsPath
import os
from ui.pages.main_page import MainPage
from tests.base import BaseCase, CampaignSegmentCase
import time


class Test(BaseCase):

    POSITIVE_AUTH_URL = 'https://target.my.com/dashboard'

    @pytest.mark.UI
    def test_auth_positive(self, account_page):
        auth_page = account_page(email="oswalth3@gmail.com", password="cpu#N7ZvD6")
        assert self.POSITIVE_AUTH_URL == auth_page.driver.current_url

    @pytest.mark.UI
    def test_auth_negative(self, account_page):
        auth_page = account_page(email="oswalth3@gmail.com", password="1111")
        assert self.POSITIVE_AUTH_URL != auth_page.driver.current_url


class TestCampaignSegment(CampaignSegmentCase):
    img_path = PureWindowsPath(Path.cwd().joinpath('static', 'img.png')).as_posix()

    @pytest.mark.UI
    def test_campaign_create(self, campaign_page):
        campaign_name = "test campaign 1"
        page = campaign_page(self.account_page)
        page.create_campaign("https://github.com/snicks92", campaign_name, self.img_path)
        time.sleep(1)
        assert page.check_if_exists(page.locators.CAMPAIGN_LOCATOR, campaign_name)

    @pytest.mark.UI
    def test_audience_create(self, audience_page):
        segment_name = "test segment to add"
        page = audience_page(self.account_page)
        page.create_segment(segment_name)
        time.sleep(1)
        assert page.check_if_exists(page.locators.SEGMENT_LOCATOR, segment_name)

    @pytest.mark.UI
    def test_audience_delete(self, audience_page):
        segment_name = "test segment to delete"
        page = audience_page(self.account_page)

        page.create_segment(segment_name)
        page.delete_segment(segment_name)
        time.sleep(1)
        assert not page.check_if_exists(page.locators.SEGMENT_LOCATOR, segment_name)

