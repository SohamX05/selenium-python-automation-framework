"""Assignment 3: CSS Selector Challenge.

Locate elements with CSS selectors, including wildcard attribute selectors
for partially known / dynamic attribute values:
    ^=  starts with     *=  contains     $=  ends with
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import BASE_URL, LOGIN_URL, create_driver, wait


def main():
    driver = create_driver()
    try:
        driver.get(LOGIN_URL)
        wait(driver).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#input-email")))

        # Plain CSS selectors: id, attribute, class
        print("#input-email                      ->", driver.find_element(By.CSS_SELECTOR, "#input-email").get_attribute("name"))
        print("input[name='password']            ->", driver.find_element(By.CSS_SELECTOR, "input[name='password']").get_attribute("id"))
        print("input.btn.btn-primary             ->", driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary").get_attribute("value"))

        # Wildcard: every element whose id STARTS WITH 'input-'
        # (same idea as the "id starts with user_" example; this site prefixes form ids with 'input-')
        starts_with = driver.find_elements(By.CSS_SELECTOR, "input[id^='input-']")
        ids = [element.get_attribute("id") for element in starts_with]
        print("input[id^='input-']               ->", ids)
        assert ids == ["input-email", "input-password"]

        driver.get(BASE_URL)
        wait(driver).until(EC.visibility_of_element_located((By.ID, "menu")))

        # Wildcard: href CONTAINS a value
        category_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='route=product/category']")
        print(f"a[href*='route=product/category'] -> {len(category_links)} category links")
        assert len(category_links) > 0

        # Wildcard: href ENDS WITH a value
        cart_link = driver.find_element(By.CSS_SELECTOR, "a[href$='route=checkout/cart']")
        print("a[href$='route=checkout/cart']    ->", cart_link.get_attribute("title"))

        # Wildcard: class CONTAINS a value
        products = driver.find_elements(By.CSS_SELECTOR, "div[class*='product-layout']")
        print(f"div[class*='product-layout']      -> {len(products)} featured products")
        assert len(products) == 4

        cart_link.click()
        wait(driver).until(EC.url_contains("route=checkout/cart"))
        print("Clicked cart link ->", driver.title)
        print("Assignment 3 PASSED")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
