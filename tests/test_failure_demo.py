"""Intentionally failing test that proves screenshots are taken on failure.

Skipped by default. Run it with:
    pytest tests/test_failure_demo.py --run-failure-demo --html=report.html --self-contained-html
"""
import pytest

from pages.home_page import HomePage


@pytest.mark.failure_demo
def test_screenshot_is_captured_on_failure(driver):
    results_page = HomePage(driver).open().search_for("MacBook")
    assert "Product That Does Not Exist" in results_page.product_names()
