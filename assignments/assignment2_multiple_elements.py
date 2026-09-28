"""Assignment 2: Multiple Element Identification.

Use find_elements() to work with lists of elements:
all links on the home page, the top menu categories and the featured products.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import BASE_URL, create_driver, wait


def main():
    driver = create_driver()
    try:
        driver.get(BASE_URL)
        wait(driver).until(EC.visibility_of_element_located((By.ID, "menu")))

        # 1. All links on the page and their text
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Total <a> tags on the home page: {len(links)}")
        visible_links = [link for link in links if link.text.strip()]
        print(f"Links with visible text: {len(visible_links)}")
        for number, link in enumerate(visible_links, start=1):
            print(f"  {number:>2}. {link.text.strip():<30} {link.get_attribute('href')}")

        # 2. Top menu categories
        categories = driver.find_elements(By.CSS_SELECTOR, "#menu ul.nav > li > a")
        names = [category.text.strip() for category in categories]
        print("\nMenu categories:", names)
        assert "Desktops" in names and "Cameras" in names

        # 3. Featured products and their prices
        print("\nFeatured products:")
        for product in driver.find_elements(By.CSS_SELECTOR, ".product-layout .caption"):
            name = product.find_element(By.TAG_NAME, "h4").text
            price = product.find_element(By.CLASS_NAME, "price").text.splitlines()[0]
            print(f"  {name:<25} {price}")

        assert len(visible_links) > 0
        print("\nAssignment 2 PASSED")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
