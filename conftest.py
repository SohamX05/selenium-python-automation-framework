"""Shared PyTest fixtures and hooks.

- driver:            opens a browser (settings from config.ini) and always quits it
- registered_user:   creates a fresh throwaway account for the valid-login test
- screenshot hook:   saves a screenshot automatically when a test fails and
                     embeds it in the pytest-html report
"""
import base64

import pytest
from selenium import webdriver

from pages.register_page import RegisterPage
from pages.account_page import AccountPage
from utils.config_reader import config
from utils.data_helper import unique_email, unique_id
from utils.screenshot import take_screenshot


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=None,
                     help="Override browser from config.ini (chrome or edge)")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run the browser without a visible window")
    parser.addoption("--run-failure-demo", action="store_true", default=False,
                     help="Run the intentionally failing screenshot demo test")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-failure-demo"):
        return
    skip = pytest.mark.skip(reason="failure demo; enable with --run-failure-demo")
    for item in items:
        if "failure_demo" in item.keywords:
            item.add_marker(skip)


def _create_driver(browser_name, headless):
    """Create a WebDriver. Selenium Manager downloads the driver automatically."""
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        driver_class = webdriver.Chrome
    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        driver_class = webdriver.Edge
    else:
        raise ValueError(f"Unsupported browser '{browser_name}'. Use chrome or edge.")

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    return driver_class(options=options)


@pytest.fixture
def driver(request):
    browser_name = (request.config.getoption("--browser") or config.browser).lower()
    headless = request.config.getoption("--headless") or config.headless

    driver = _create_driver(browser_name, headless)
    if not headless:
        driver.maximize_window()
    driver.get(config.base_url)
    yield driver
    driver.quit()


@pytest.fixture
def registered_user(driver):
    """Register a brand-new account and log out, returning its credentials.

    The public demo has no official credentials, so each run creates its own
    account with a unique e-mail. Nothing personal is stored anywhere.
    """
    user = {
        "email": unique_email("capstone"),
        "password": f"Test@{unique_id()}",
    }
    RegisterPage(driver).open().register(
        first_name="Capstone",
        last_name="Tester",
        email=user["email"],
        telephone="9000000000",
        password=user["password"],
    )
    AccountPage(driver).logout()  # registration logs the user in automatically
    return user


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only react to failures in the test body (or its setup), not teardown.
    if report.when not in ("setup", "call") or not report.failed:
        return
    driver = item.funcargs.get("driver")
    if driver is None:
        return

    try:
        file_path = take_screenshot(driver, item.name)
    except Exception as error:  # the browser may already be gone
        report.sections.append(("screenshot", f"Could not take screenshot: {error}"))
        return

    report.sections.append(("screenshot", f"Saved to {file_path}"))

    # Embed the screenshot into the pytest-html report when it is installed.
    html_plugin = item.config.pluginmanager.getplugin("html")
    if html_plugin is not None:
        image = base64.b64encode(file_path.read_bytes()).decode()
        extras = getattr(report, "extras", [])
        extras.append(html_plugin.extras.png(image, name=file_path.name))
        report.extras = extras
