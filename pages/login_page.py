"""Login page (index.php?route=account/login)."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    ROUTE = "index.php?route=account/login"

    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger")

    def open(self):
        self.open_route(self.ROUTE)
        self.find(self.EMAIL_INPUT)
        return self

    def is_displayed(self):
        return self.find(self.LOGIN_BUTTON).is_displayed()

    def login(self, email, password):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def error_message(self):
        # The alert contains a close "x" button, so keep only the first line.
        return self.get_text(self.ERROR_ALERT).splitlines()[0].strip()
