"""Reads test data from CSV files in the data/ folder using the csv module."""
import csv

from utils.paths import DATA_DIR


def read_csv(file_name):
    """Return the rows of data/<file_name> as a list of dictionaries.

    The first row of the CSV is treated as the header, so each row becomes
    e.g. {"search_term": "MacBook", "expected_product": "MacBook Air", ...}.
    """
    file_path = DATA_DIR / file_name
    with open(file_path, newline="", encoding="utf-8") as csv_file:
        return [
            {key.strip(): (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(csv_file)
        ]


def to_bool(value):
    """Convert CSV text such as 'true', 'yes', '1' to a Python bool."""
    return str(value).strip().lower() in {"true", "yes", "y", "1"}
