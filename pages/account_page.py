"""My Account page shown after a successful login, plus logout."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AccountPage(BasePage):
    LOGOUT_ROUTE = "index.php?route=account/logout"

    MY_ACCOUNT_HEADING = (By.XPATH, "//div[@id='content']/h2[normalize-space()='My Account']")
    LOGOUT_LINK = (By.CSS_SELECTOR, "#column-right a[href*='route=account/logout']")

    def wait_until_loaded(self):
        self.wait_for_url_contains("route=account/account")
        self.find(self.MY_ACCOUNT_HEADING)
        return self

    def is_logged_in(self):
        return self.find(self.LOGOUT_LINK).is_displayed()

    def logout(self):
        self.open_route(self.LOGOUT_ROUTE)
        self.wait_for_url_contains("route=account/logout")
