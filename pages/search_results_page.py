"""Search results page (index.php?route=product/search)."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "#content h1")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-thumb h4 a")
    SEARCH_CRITERIA_INPUT = (By.ID, "input-search")
    NO_RESULTS_MESSAGE = (
        By.XPATH,
        "//div[@id='content']/p[contains(., 'There is no product that matches')]",
    )

    def wait_until_loaded(self, search_term):
        self.wait_for_url_contains("route=product/search")
        self.wait.until(lambda d: search_term in self.get_text(self.HEADING))
        return self

    @property
    def heading(self):
        return self.get_text(self.HEADING)

    @property
    def search_criteria(self):
        return self.find(self.SEARCH_CRITERIA_INPUT).get_attribute("value")

    def product_names(self):
        return [element.text.strip() for element in self.find_all(self.PRODUCT_NAMES)]

    def no_results_message(self):
        return self.get_text(self.NO_RESULTS_MESSAGE)
