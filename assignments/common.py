"""Shared setup for the assignment scripts: browser creation and waits."""
import sys

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://tutorialsninja.com/demo/"
LOGIN_URL = BASE_URL + "index.php?route=account/login"
TIMEOUT = 10


def create_driver():
    """Start Chrome (Selenium Manager finds the driver). Pass --headless to hide it."""
    options = webdriver.ChromeOptions()
    if "--headless" in sys.argv:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    return webdriver.Chrome(options=options)


def wait(driver):
    return WebDriverWait(driver, TIMEOUT)


def show(label, element):
    """Print a one-line description of a located element."""
    text = element.text.strip() or element.get_attribute("value") or ""
    print(f"  {label:<38} <{element.tag_name}> id='{element.get_attribute('id')}' "
          f"name='{element.get_attribute('name')}' text='{text[:40]}'")
