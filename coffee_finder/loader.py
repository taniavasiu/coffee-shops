"""Fetching and parsing shop data.

Responsibility: turn an external data source (URL or local file) into a
list of validated `Shop` objects.
"""
import csv
from io import StringIO
from typing import List
from urllib.request import urlopen

from .shop import Shop


class MalformedShopDataError(Exception):
   
def fetch_csv(url: str, timeout: int = 10) -> str:
    if url.startswith(("http://", "https://")):
        with urlopen(url, timeout=timeout) as response:
            return response.read().decode("utf-8")
    with open(url, "r", encoding="utf-8") as f:
        return f.read()


def parse_shops(csv_text: str) -> List[Shop]:
    """Parse CSV text into Shop objects.

    CSV format per row: `Name,Y Coordinate,X Coordinate`
    """
    shops: List[Shop] = []
    # csv.reader handles quoting, escaping and commas-inside-fields
    reader = csv.reader(StringIO(csv_text))

    for lineno, row in enumerate(reader, start=1):
        if not row or (len(row) == 1 and row[0].strip() == ""):
            continue

        if len(row) != 3:
            raise MalformedShopDataError(
                f"Line {lineno}: expected 3 fields, got {len(row)}: {row!r}"
            )

        # Validation 1: Strip whitespace defensively — some CSVs have " value" with
        # leading spaces that would break float() parsing.
        name, y_str, x_str = (field.strip() for field in row)

        # Validation 2: name must be non-empty — a shop with no name is
        # useless for display.
        if not name:
            raise MalformedShopDataError(f"Line {lineno}: empty shop name")

        # Validation 3: coordinates must be numeric. We catch ValueError
        # from float() and re-raise as our domain exception so the caller
        # only has to handle one error type.
        try:
            y = float(y_str)
            x = float(x_str)
        except ValueError as exc:
            raise MalformedShopDataError(
                f"Line {lineno}: invalid coordinates: {row!r}"
            ) from exc

        shops.append(Shop(name=name, x=x, y=y))

    return shops


def load_shops(url: str) -> List[Shop]:
    return parse_shops(fetch_csv(url))
