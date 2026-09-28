"""Login scenarios for TutorialsNinja demo."""
import pytest

from pages.account_page import AccountPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.csv_reader import read_csv
from utils.data_helper import fill_placeholders

INVALID_LOGIN_DATA = read_csv("login_data.csv")


@pytest.mark.login
def test_login_page_opens_from_home_menu(driver):
    home = HomePage(driver).open()
    home.go_to_login()

    login_page = LoginPage(driver)
    assert login_page.is_displayed()
    assert login_page.title == "Account Login"


@pytest.mark.login
@pytest.mark.parametrize(
    "row", INVALID_LOGIN_DATA, ids=[row["scenario"] for row in INVALID_LOGIN_DATA]
)
def test_invalid_login_shows_error(driver, row):
    login_page = LoginPage(driver).open()

    login_page.login(fill_placeholders(row["email"]), row["password"])

    assert login_page.error_message() == row["expected_message"]
    assert "route=account/login" in driver.current_url  # still on login page


@pytest.mark.login
@pytest.mark.registration
def test_valid_login_with_fresh_account(driver, registered_user):
    login_page = LoginPage(driver).open()

    login_page.login(registered_user["email"], registered_user["password"])

    account_page = AccountPage(driver).wait_until_loaded()
    assert account_page.title == "My Account"
    assert account_page.is_logged_in()
