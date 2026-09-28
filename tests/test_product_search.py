"""Product search scenarios driven by data/test_data.csv."""
import pytest

from pages.home_page import HomePage
from utils.csv_reader import read_csv, to_bool

SEARCH_DATA = read_csv("test_data.csv")


@pytest.mark.search
@pytest.mark.parametrize(
    "row", SEARCH_DATA, ids=[row["search_term"] for row in SEARCH_DATA]
)
def test_product_search(driver, row):
    search_term = row["search_term"]

    results_page = HomePage(driver).open().search_for(search_term)

    assert results_page.heading == f"Search - {search_term}"
    assert results_page.search_criteria == search_term

    products = results_page.product_names()
    if to_bool(row["expect_results"]):
        assert row["expected_product"] in products, f"Found: {products}"
        assert all(search_term.lower() in name.lower() for name in products), (
            f"Every result should contain '{search_term}': {products}"
        )
    else:
        assert products == []
        assert results_page.no_results_message() == (
            "There is no product that matches the search criteria."
        )
