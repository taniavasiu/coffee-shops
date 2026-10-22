"""Unit tests for CSV parsing and validation.

We test parse_shops directly with in-memory strings. This avoids any
network or filesystem dependency, keeping tests fast and deterministic.
"""
import pytest

from coffee_finder.loader import MalformedShopDataError, parse_shops


def test_parse_valid_csv():
    # Happy path: well-formed CSV with two rows.
    # Also verifies the Name,Y,X column order from the challenge spec.
    csv_text = (
        "Starbucks Seattle,47.5809,-122.3160\n"
        "Starbucks SF,37.7749,-122.4194\n"
    )
    shops = parse_shops(csv_text)
    assert len(shops) == 2
    assert shops[0].name == "Starbucks Seattle"
    assert shops[0].y == 47.5809
    assert shops[0].x == -122.3160


def test_parse_skips_blank_lines():
    # CSVs often have stray empty lines (e.g. trailing newline).
    # These must not become ghost Shop entries or raise errors.
    csv_text = "A,1,2\n\nB,3,4\n"
    assert len(parse_shops(csv_text)) == 2


def test_parse_bad_field_count_raises():
    # Wrong number of columns → malformed row → must raise.
    # The challenge requires exiting on malformed data, not skipping.
    with pytest.raises(MalformedShopDataError):
        parse_shops("OnlyName,1\n")


def test_parse_non_numeric_coords_raises():
    # Coordinates that aren't numbers → must raise.
    with pytest.raises(MalformedShopDataError):
        parse_shops("Shop,abc,2\n")


def test_parse_empty_name_raises():
    # Empty shop name → must raise (a shop needs a name for display).
    with pytest.raises(MalformedShopDataError):
        parse_shops(",1,2\n")
