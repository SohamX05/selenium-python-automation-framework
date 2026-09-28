# Selenium Python Automation Framework

Capstone Assignment 2 — Selenium Python Framework Development (Unittest + PyTest + POM)

**Soham Mondal** · Enrollment No. 12023002001361 · CSE, IEM Kolkata · Project Guide: Sramana Mukherjee

## Submission

- Report: [`submission/Selenium_Capstone_Submission.pdf`](submission/Selenium_Capstone_Submission.pdf) (editable: `.docx`)
- Evidence screenshots: [`submission/screenshots/`](submission/screenshots/)
- HTML test report: [`report.html`](report.html) · failure demo report: [`submission/failure_report.html`](submission/failure_report.html) (GitHub shows HTML files as source code; download and open them in a browser, or see the screenshots)
- Latest run (27 Sep 2026, Windows, Python 3.11.4): **19 passed, 1 skipped** (the opt-in failure demo)
- Certifications: [`certifications/`](certifications/)
- Locator assignments 1–4: [`assignments/`](assignments/)

`capture_evidence.py` regenerates the step-by-step screenshots of the live site.

## Objective

Automate the **Login** and **Product Search** features of an e-commerce demo site,
[TutorialsNinja Demo](https://tutorialsninja.com/demo/), using Selenium WebDriver with Python
in a reusable, scalable framework.

## Technologies

- Python 3.9+
- Selenium 4 (Selenium Manager downloads the browser driver automatically)
- PyTest (main test runner)
- Unittest (utility tests)
- Page Object Model (POM)
- CSV test data (`csv` module)
- pytest-html (HTML reports)

## Project Structure

```text
selenium-python-automation-framework/
├── config/
│   └── config.ini            # base URL, browser, timeout, headless, screenshot folder
├── data/
│   ├── test_data.csv         # product search data (term, expected product, results expected?)
│   └── login_data.csv        # invalid-login scenarios and expected error message
├── pages/                    # Page Object Model
│   ├── base_page.py          # shared helpers: explicit waits, click, type, get text
│   ├── home_page.py          # header search box + My Account menu
│   ├── search_results_page.py# results heading, product names, "no results" message
│   ├── login_page.py         # e-mail, password, Login button, error alert
│   ├── register_page.py      # creates a throwaway account for the valid-login test
│   └── account_page.py       # "My Account" page after login, logout
├── tests/
│   ├── test_login.py         # login scenarios
│   ├── test_product_search.py# CSV-driven search scenarios
│   └── test_failure_demo.py  # intentionally failing test (skipped by default)
├── utils/
│   ├── config_reader.py      # reads config.ini
│   ├── csv_reader.py         # reads CSV files into dictionaries
│   ├── screenshot.py         # saves uniquely named screenshots
│   ├── data_helper.py        # unique e-mails / ids for test data
│   └── paths.py              # project-relative paths (no absolute paths)
├── screenshots/              # failure screenshots are saved here
├── assignments/              # locator assignments 1–4 (scripts + README)
├── certifications/           # completed course certificates
├── submission/               # report (PDF/DOCX), evidence screenshots, console output
├── capture_evidence.py       # captures the evidence screenshots
├── conftest.py               # driver fixture, account fixture, screenshot-on-failure hook
├── pytest.ini                # discovery, markers, default options
├── requirements.txt
├── unittest_demo.py          # unittest.TestCase tests for the utilities
└── README.md
```

## Setup (Windows)

Requirements: Python 3.9+ and Google Chrome (or Microsoft Edge). No manual ChromeDriver download is needed.

```bash
git clone https://github.com/SohamX05/selenium-python-automation-framework.git
cd selenium-python-automation-framework
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Activation depends on the terminal:

- Command Prompt / PowerShell: `venv\Scripts\activate`
- Git Bash: `source venv/Scripts/activate`
- macOS/Linux: `source venv/bin/activate`

The prompt shows `(venv)` when it is active.

## Execution

Run everything (PyTest + the unittest file):

```bash
pytest -v
```

HTML report:

```bash
pytest -v --html=report.html --self-contained-html
```

Unittest on its own:

```bash
python unittest_demo.py
```

Useful options:

```bash
pytest -v -m search                  # only search tests
pytest -v -m login                   # only login tests
pytest -v -m "not registration"      # skip the test that creates an account
pytest -v --headless                 # no visible browser window
pytest -v --browser edge             # use Edge instead of Chrome
```

## Test Scenarios

### Login (`tests/test_login.py`)

| Test | Steps | Expected result |
|---|---|---|
| `test_login_page_opens_from_home_menu` | Home → My Account → Login | Login form shown, title "Account Login" |
| `test_invalid_login_shows_error` (3 rows from `login_data.csv`) | Enter e-mail/password from CSV → Login | Alert "Warning: No match for E-Mail Address and/or Password.", user stays on login page |
| `test_valid_login_with_fresh_account` | Register a new unique account → logout → login with it | "My Account" page opens and Logout link is visible |

**Chosen login approach.** TutorialsNinja does not publish demo credentials, so no working
credentials are hard-coded. Instead:

1. Negative login is tested with CSV data. E-mails contain a `{uid}` placeholder that is replaced
   with a random id each run, because OpenCart temporarily locks an e-mail after repeated failed logins.
2. Positive login uses the `registered_user` fixture, which registers a brand-new account through the
   site's public registration form (unique `@example.com` e-mail, random password), logs out, and then
   the test logs in with it. This is deterministic and does not depend on anyone's personal account.

### Product Search (`tests/test_product_search.py`)

Each row of `data/test_data.csv` becomes one test:

1. Open home page
2. Type the `search_term` in the header search box and click the search button
3. Wait for the results page
4. Verify the heading is `Search - <term>` and the search box keeps the term
5. If `expect_results` is `true`: the `expected_product` is in the results and every result name contains the term
6. If `false`: no products are listed and "There is no product that matches the search criteria." is shown

## Screenshot Handling

`conftest.py` implements the `pytest_runtest_makereport` hook. When a test fails (in setup or in the
test body) and it uses the `driver` fixture, the hook:

1. saves `screenshots/<test_name>_<YYYYmmdd_HHMMSS_micro>.png` (the timestamp prevents overwriting,
   and characters like `[ ]` are replaced so the name is valid on Windows);
2. embeds the same image in the pytest-html report.

Demonstrate it with the intentionally failing test:

```bash
pytest tests/test_failure_demo.py --run-failure-demo -v --html=report.html --self-contained-html
```

## Reporting

`pytest-html` generates `report.html` with a summary, pass/fail per test, durations, logs and
(for failures) the embedded screenshot. `--self-contained-html` puts CSS and images inside the
single file so it can be shared or submitted.

## POM Explanation

Each page has its own class that stores its locators and exposes actions such as
`login(email, password)` or `search_for(product)`. Tests only call these methods, so:

- locators live in one place — if the site changes, only the page class changes;
- tests read like business steps and are easy to understand;
- common Selenium code (waits, clicks, typing) lives once in `BasePage`.

## Configuration

All environment values are in `config/config.ini`; nothing is hard-coded in the tests.
`--browser` and `--headless` command-line options can override the file for a single run.
No credentials are required.

## Limitations / Demo-site considerations

- Tests depend on the public TutorialsNinja site being online and on its current product catalogue.
- The valid-login test creates one new throwaway account on the demo site per run. Deselect it with
  `-m "not registration"` if you prefer not to.
- The site has no official test credentials, so a pre-existing valid account is not used.
- Repeated failed logins for the same e-mail can be locked for an hour by the site; unique e-mails avoid this.
- Only Chrome and Edge are configured, which covers typical Windows machines.
