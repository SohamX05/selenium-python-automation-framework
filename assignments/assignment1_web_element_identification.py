"""Assignment 1: Web Element Identification.

Locate elements on the TutorialsNinja login page using
By.ID, By.NAME, By.TAG_NAME, By.LINK_TEXT and By.CLASS_NAME.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import LOGIN_URL, create_driver, show, wait


def main():
    driver = create_driver()
    try:
        driver.get(LOGIN_URL)
        print("Page:", driver.title)

        # By.ID -> the e-mail (username) field
        email = wait(driver).until(EC.visibility_of_element_located((By.ID, "input-email")))
        show("By.ID 'input-email'", email)

        # By.NAME -> the password field
        password = driver.find_element(By.NAME, "password")
        show("By.NAME 'password'", password)

        # By.TAG_NAME -> the section headings on the page
        headings = driver.find_elements(By.TAG_NAME, "h2")
        print("  By.TAG_NAME 'h2'                      ->", [h.text for h in headings])

        # By.CLASS_NAME -> all Bootstrap text inputs
        inputs = driver.find_elements(By.CLASS_NAME, "form-control")
        print("  By.CLASS_NAME 'form-control'          ->", [i.get_attribute("name") for i in inputs])

        # By.LINK_TEXT -> the "Forgotten Password" link
        forgotten = driver.find_element(By.LINK_TEXT, "Forgotten Password")
        show("By.LINK_TEXT 'Forgotten Password'", forgotten)

        # Interact to prove the elements are the right ones
        email.send_keys("student@example.com")
        password.send_keys("secret123")
        assert email.get_attribute("value") == "student@example.com"
        assert password.get_attribute("type") == "password"
        assert [h.text for h in headings] == ["New Customer", "Returning Customer"]

        forgotten.click()
        wait(driver).until(EC.url_contains("route=account/forgotten"))
        print("  Clicked link ->", driver.title)
        print("Assignment 1 PASSED")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
