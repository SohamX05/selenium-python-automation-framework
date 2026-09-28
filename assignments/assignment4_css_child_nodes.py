"""Assignment 4: Child Nodes Using CSS.

Locate nested elements with the CSS child combinator (parent > child)
and interact with them.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import BASE_URL, create_driver, wait


def main():
    driver = create_driver()
    try:
        driver.get(BASE_URL)

        # 1. The search button is a <button> inside <span> inside <div id="search">
        search_box = wait(driver).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#search > input")))
        search_button = driver.find_element(By.CSS_SELECTOR, "div#search > span > button")
        search_box.send_keys("iPhone")
        search_button.click()
        heading = wait(driver).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#content > h1")))
        print("div#search > span > button  -> clicked, page heading:", heading.text)
        assert heading.text == "Search - iPhone"

        # 2. Product names are <a> inside <h4> inside the product caption
        names = [a.text for a in driver.find_elements(By.CSS_SELECTOR, "div.caption > h4 > a")]
        print("div.caption > h4 > a        ->", names)
        assert "iPhone" in names

        # 3. The cart button is a direct child <button> of <div id="cart">
        driver.get(BASE_URL)
        cart_button = wait(driver).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div#cart > button")))
        print("div#cart > button           ->", cart_button.text)
        cart_button.click()
        message = wait(driver).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div#cart > ul.dropdown-menu p.text-center")))
        print("Cart dropdown message       ->", message.text)
        assert message.text == "Your shopping cart is empty!"

        # 4. Footer column headings: <h5> directly inside each footer column
        footer = [h5.text for h5 in driver.find_elements(By.CSS_SELECTOR, "footer div.col-sm-3 > h5")]
        print("footer div.col-sm-3 > h5    ->", footer)
        assert len(footer) == 4

        print("Assignment 4 PASSED")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
