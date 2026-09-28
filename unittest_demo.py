"""Unittest examples for the framework's utility classes.

These run without a browser, so they are fast. Run with either:
    python unittest_demo.py
    pytest unittest_demo.py -v      (PyTest also discovers unittest.TestCase)
"""
import re
import unittest
from datetime import datetime

from utils.config_reader import config
from utils.csv_reader import read_csv, to_bool
from utils.data_helper import fill_placeholders, unique_email
from utils.screenshot import build_screenshot_name


class TestConfigReader(unittest.TestCase):
    def test_base_url_is_https_and_ends_with_slash(self):
        self.assertTrue(config.base_url.startswith("https://"))
        self.assertTrue(config.base_url.endswith("/"))

    def test_timeout_is_positive_integer(self):
        self.assertIsInstance(config.timeout, int)
        self.assertGreater(config.timeout, 0)

    def test_browser_is_supported(self):
        self.assertIn(config.browser, ("chrome", "edge"))


class TestCsvReader(unittest.TestCase):
    def test_search_data_has_required_columns(self):
        rows = read_csv("test_data.csv")
        self.assertGreater(len(rows), 0)
        for row in rows:
            self.assertEqual(
                set(row), {"search_term", "expected_product", "expect_results"}
            )
            self.assertTrue(row["search_term"])

    def test_login_data_has_expected_message(self):
        for row in read_csv("login_data.csv"):
            self.assertTrue(row["expected_message"].startswith("Warning:"))

    def test_to_bool(self):
        self.assertTrue(to_bool("true"))
        self.assertTrue(to_bool(" YES "))
        self.assertFalse(to_bool("false"))
        self.assertFalse(to_bool(""))


class TestDataHelper(unittest.TestCase):
    def test_placeholder_is_replaced(self):
        self.assertEqual(fill_placeholders("user_{uid}@example.com", "abc"),
                         "user_abc@example.com")

    def test_unique_emails_differ(self):
        self.assertNotEqual(unique_email(), unique_email())
        self.assertTrue(unique_email("x").endswith("@example.com"))


class TestScreenshotName(unittest.TestCase):
    def test_name_is_windows_safe_and_timestamped(self):
        name = build_screenshot_name(
            "test_product_search[MacBook Air]", datetime(2026, 9, 27, 10, 30, 5, 42)
        )
        self.assertEqual(name, "test_product_search_MacBook_Air_20260927_103005_000042.png")
        self.assertIsNone(re.search(r'[<>:"/\\|?*\[\] ]', name))


if __name__ == "__main__":
    unittest.main(verbosity=2)
