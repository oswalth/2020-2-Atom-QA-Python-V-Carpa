from selenium.webdriver.common.by import By


class BasePageLocators:
    pass


class MainPageLocators(BasePageLocators):
    LOGIN_BUTTON = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')
    EMAIL_INPUT = (By.XPATH, '//input[@name="email" and contains(@class, "authForm") and @type="text"]')
    PASSWORD_INPUT = (By.XPATH, '//input[@name="password" and contains(@class, "authForm") and @type="password"]')
    CONFIRM_LOGIN_BUTTON = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')


class AccountPageLocators(BasePageLocators):
    # Локаторы хедера
    HEADER_CAMPAIGN_BUTTON = (By.XPATH, '//a[@href="/dashboard"]')
    HEADER_AUDIENCE_BUTTON = (By.XPATH, '//a[@href="/segments"]')


class CampaignPageLocators(AccountPageLocators):
    CREATE_CAMPAIGN_BUTTON = (By.XPATH, '//div[contains(@class,"button-module-textWrapper") and text()="Создать '
                                        'кампанию"]')
    TRAFFIC_LOCATOR = (By.XPATH, '//div[@class="column-list-item _traffic"]')
    URL_INPUT = (By.XPATH, '//input[contains(@class, "mainUrl-module-searchInput")]')
    BANNER_ADS = (By.XPATH, '//div[@data-id="patterns_4"]')
    IMG_INPUT = (By.XPATH, '//div[contains(@class, "roles-module-buttonWrap")]/div/input[@type="file"]')
    SUBMIT_IMG = (By.XPATH, '//input[contains(@class, "image-cropper")]')
    CAMPAIGN_NAME_INPUT = (By.XPATH, '//div[contains(@class, "campaign-name__name-wrap")]//input')
    SUBMIT_CREATION = (By.XPATH, '//div[@class="footer"]//div[text()="Создать кампанию"]')
    CAMPAIGN_LOCATOR = (By.XPATH, '//a[@title="{}"]')


class AudiencePageLocators(AccountPageLocators):
    # ADD
    CREATE_SEGMENT_LINK = (By.XPATH, '//a[@href="/segments/segments_list/new/"]')
    CREATE_SEGMENT_BUTTON = (By.XPATH, '//div[text()="Создать сегмент" and contains(@class, "button")]')
    SEGMENT_DISPLAY_NONE = (By.XPATH, '//div[contains(@class, "js-create-button-wrap")][contains(@style, "display: none")]')

    APP_GAMES_LOCATOR = (By.XPATH, '//div[text()="Приложения и игры в соцсетях"]')
    SEGMENT_INPUT_CHECKBOX = (By.XPATH, '//input[contains(@class, "adding-segments-source")]')

    ADD_SEGMENT_BUTTON = (By.XPATH, '//div[@class="button__text" and text()="Добавить сегмент"]')

    SEGMENT_NAME_INPUT = (By.XPATH, '//input[@maxlength="60" and contains(@class, "input__inp")]')
    CREATE_SEGMENT_FINAL_BUTTON = (By.XPATH, '//div[contains(@class, "create-segment-form__btn-wrap")]//div')

    SEGMENT_LOCATOR = (By.XPATH, '//a[@title="{}"]')
    # DELETE
    SEGMENT_NAME_LOCATOR = (By.XPATH, '//div[contains(@class, "cells-module-name")]/a[text()="{}"]')
    SEGMENT_ID_LOCATOR = (By.XPATH, '//div[contains(@class, "segmentsTable-module-id")]/span[text()="{}"]')
    SEGMENT_DELETE_BTN = (By.XPATH, '//div[contains(@data-test, "remove-{}")]/span')
    SEGMENT_DELETE_CONFIRM = (By.XPATH, '//button[contains(@class, "button_confirm-remove")]')
