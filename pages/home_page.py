"""Home page: header search box and account menu."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage


class HomePage(BasePage):
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    MY_ACCOUNT_MENU = (By.CSS_SELECTOR, "#top-links a[title='My Account']")
    LOGIN_LINK = (By.LINK_TEXT, "Login")

    def open(self):
        self.open_route()
        self.find(self.SEARCH_INPUT)
        return self

    def search_for(self, product_name):
        self.type_text(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)
        return SearchResultsPage(self.driver).wait_until_loaded(product_name)

    def go_to_login(self):
        self.click(self.MY_ACCOUNT_MENU)
        self.click(self.LOGIN_LINK)
        self.wait_for_url_contains("route=account/login")
