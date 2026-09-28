"""Registration page, used only to create a fresh throwaway test account."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegisterPage(BasePage):
    ROUTE = "index.php?route=account/register"

    FIRST_NAME = (By.ID, "input-firstname")
    LAST_NAME = (By.ID, "input-lastname")
    EMAIL = (By.ID, "input-email")
    TELEPHONE = (By.ID, "input-telephone")
    PASSWORD = (By.ID, "input-password")
    CONFIRM_PASSWORD = (By.ID, "input-confirm")
    PRIVACY_POLICY = (By.NAME, "agree")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "input[type='submit'][value='Continue']")

    def open(self):
        self.open_route(self.ROUTE)
        self.find(self.FIRST_NAME)
        return self

    def register(self, first_name, last_name, email, telephone, password):
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.EMAIL, email)
        self.type_text(self.TELEPHONE, telephone)
        self.type_text(self.PASSWORD, password)
        self.type_text(self.CONFIRM_PASSWORD, password)
        self.click(self.PRIVACY_POLICY)
        self.click(self.CONTINUE_BUTTON)
        # Successful registration redirects to route=account/success.
        self.wait_for_url_contains("route=account/success")
