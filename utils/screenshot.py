"""Screenshot helper used by the failure hook in conftest.py."""
import re
from datetime import datetime

from utils.config_reader import config


def build_screenshot_name(test_name, now=None):
    """Create a safe, unique file name such as
    'test_search_MacBook_20260927_153012_123456.png'.

    Characters that Windows does not allow in file names (e.g. [ ] : ?)
    are replaced, and a timestamp prevents overwriting older screenshots.
    """
    now = now or datetime.now()
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", test_name).strip("_")
    return f"{safe_name}_{now:%Y%m%d_%H%M%S_%f}.png"


def take_screenshot(driver, test_name):
    """Save a screenshot of the current browser window and return its path."""
    folder = config.screenshot_dir
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / build_screenshot_name(test_name)
    driver.save_screenshot(str(file_path))
    return file_path
