"""Common actions shared by every page object."""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config_reader import config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.timeout)
        self.base_url = config.base_url

    def open_route(self, route=""):
        """Open base_url + route, e.g. 'index.php?route=account/login'."""
        self.driver.get(self.base_url + route)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text.strip()

    def wait_for_url_contains(self, fragment):
        return self.wait.until(EC.url_contains(fragment))

    @property
    def title(self):
        return self.driver.title
