"""Reads settings from config/config.ini."""
import configparser

from utils.paths import CONFIG_FILE, PROJECT_ROOT

_SECTION = "DEFAULT"


class ConfigReader:
    """Small wrapper around configparser with typed getters."""

    def __init__(self, config_file=CONFIG_FILE):
        self._parser = configparser.ConfigParser()
        if not self._parser.read(config_file, encoding="utf-8"):
            raise FileNotFoundError(f"Config file not found: {config_file}")

    def get(self, key, fallback=None):
        return self._parser.get(_SECTION, key, fallback=fallback)

    @property
    def base_url(self):
        # Always end with "/" so relative routes can be appended safely.
        return self.get("base_url").rstrip("/") + "/"

    @property
    def browser(self):
        return self.get("browser", "chrome").strip().lower()

    @property
    def timeout(self):
        return self._parser.getint(_SECTION, "timeout", fallback=10)

    @property
    def headless(self):
        return self._parser.getboolean(_SECTION, "headless", fallback=False)

    @property
    def screenshot_dir(self):
        return PROJECT_ROOT / self.get("screenshot_dir", "screenshots")


# Shared instance used across the framework.
config = ConfigReader()
