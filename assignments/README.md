# Selenium Locator Assignments

Four short Selenium Python scripts covering element identification, all run against
[TutorialsNinja Demo](https://tutorialsninja.com/demo/) (the same site as the capstone framework).
Each script prints what it found, interacts with the elements, and checks the result with `assert`.
It ends with `Assignment N PASSED` when everything worked.

## How to run

From the project root, with the virtual environment active:

```bash
python assignments/assignment1_web_element_identification.py
python assignments/assignment2_multiple_elements.py
python assignments/assignment3_css_selectors.py
python assignments/assignment4_css_child_nodes.py
```

Add `--headless` to any command to run without a visible browser window.

## Files

| File | Purpose |
|---|---|
| `common.py` | Shared Chrome setup, base URL, explicit-wait helper |
| `assignment1_web_element_identification.py` | Assignment 1 |
| `assignment2_multiple_elements.py` | Assignment 2 |
| `assignment3_css_selectors.py` | Assignment 3 |
| `assignment4_css_child_nodes.py` | Assignment 4 |

## Assignment 1: Web Element Identification

**Task:** locate elements using `By.ID`, `By.NAME`, `By.TAG_NAME`, `By.LINK_TEXT` and `By.CLASS_NAME`.

Page: the login page.

| Locator | Value | Element found |
|---|---|---|
| `By.ID` | `input-email` | E-mail (username) field |
| `By.NAME` | `password` | Password field |
| `By.TAG_NAME` | `h2` | "New Customer", "Returning Customer" headings |
| `By.CLASS_NAME` | `form-control` | All text inputs (search, email, password) |
| `By.LINK_TEXT` | `Forgotten Password` | Forgotten-password link |

The script types into the e-mail and password fields, checks the values, then clicks the link and confirms the forgotten-password page opens.

## Assignment 2: Multiple Element Identification

**Task:** find several elements of the same type and work with the list.

- `find_elements(By.TAG_NAME, "a")` collects every link on the home page; the script prints the text and URL of each link that has visible text.
- `#menu ul.nav > li > a` lists the top menu categories.
- For each featured product (`.product-layout .caption`), the script finds the name and price inside it.

## Assignment 3: CSS Selector Challenge

**Task:** use CSS selectors, including wildcards for partial or dynamic attribute values.

| Selector | Meaning | Result |
|---|---|---|
| `#input-email` | id | E-mail field |
| `input[name='password']` | attribute | Password field |
| `input.btn.btn-primary` | tag + classes | Login button |
| `input[id^='input-']` | id **starts with** | `input-email`, `input-password` |
| `a[href*='route=product/category']` | href **contains** | All category links |
| `a[href$='route=checkout/cart']` | href **ends with** | Shopping Cart link |
| `div[class*='product-layout']` | class **contains** | The 4 featured products |

The assignment's example uses ids starting with `user_`. This site doesn't have any, but it prefixes its form field ids with `input-`, so `[id^='input-']` shows the same technique.

## Assignment 4: Child Nodes Using CSS

**Task:** locate nested elements with the CSS child combinator (`>`) and interact with them.

| Selector | Interaction |
|---|---|
| `div#search > input` | Type "iPhone" |
| `div#search > span > button` | Click the search button inside the search `div`; the results page shows "Search - iPhone" |
| `div.caption > h4 > a` | Read product names from the results |
| `div#cart > button` | Click the cart button inside the cart `div`; the dropdown shows "Your shopping cart is empty!" |
| `footer div.col-sm-3 > h5` | Read the four footer column headings |
