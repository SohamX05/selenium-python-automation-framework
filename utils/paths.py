"""Project-relative paths, so nothing depends on where the project is copied."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "config.ini"
DATA_DIR = PROJECT_ROOT / "data"
