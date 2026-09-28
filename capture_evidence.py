"""Capture step-by-step screenshots of the automated flows for the submission report.

Uses the same page objects as the tests. Screenshots are saved to
submission/screenshots/. Run from the project root:
    python capture_evidence.py
"""
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.account_page import AccountPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.data_helper import unique_email, unique_id

OUT_DIR = Path(__file__).resolve().parent / "submission" / "screenshots"


def save(driver, name, element_locator=None):
    """Scroll the element of interest into view (if given) and save a screenshot."""
    if element_locator:
        element = driver.find_element(*element_locator)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    path = OUT_DIR / f"{name}.png"
    driver.save_screenshot(str(path))
    print(f"saved {path.relative_to(OUT_DIR.parent.parent)}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1366,900")
    driver = webdriver.Chrome(options=options)
    try:
        home = HomePage(driver).open()
        save(driver, "01_home_page")

        home.type_text(home.SEARCH_INPUT, "MacBook")
        save(driver, "02_search_term_entered")

        results = HomePage(driver).open().search_for("MacBook")
        save(driver, "03_search_results_macbook", results.PRODUCT_NAMES)

        results = HomePage(driver).open().search_for("xyznonexistentproduct")
        save(driver, "04_search_no_results", results.NO_RESULTS_MESSAGE)

        login = LoginPage(driver).open()
        save(driver, "05_login_page")

        login.login(unique_email("unregistered"), "WrongPass@123")
        login.error_message()  # waits for the alert
        save(driver, "06_invalid_login_error")

        email, password = unique_email("capstone"), f"Test@{unique_id()}"
        RegisterPage(driver).open().register("Capstone", "Tester", email, "9000000000", password)
        save(driver, "07_registration_success", (By.CSS_SELECTOR, "#content h1"))
        AccountPage(driver).logout()

        LoginPage(driver).open().login(email, password)
        AccountPage(driver).wait_until_loaded()
        save(driver, "08_valid_login_my_account")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
