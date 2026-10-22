"""CLI entry point.

Run with: `python -m coffee_finder <user_x> <user_y> <shop_data_url>`

"""
from __future__ import annotations

import sys
from urllib.error import URLError

from .finder import closest_shops
from .loader import MalformedShopDataError, load_shops

USAGE = "Usage: python -m coffee_finder <user_x> <user_y> <shop_data_url>"


def main(argv: list[str]) -> int:
    """Program entry. Returns a POSIX-style exit code.

    Exit codes follow convention:
      0 = success
      1 = runtime error (bad data, network/file failure)
      2 = usage error (wrong args)
    Separating 1 vs 2 lets shell scripts react differently.
    """
    # argv[0] is the script name itself, so we expect 4 elements total.
    if len(argv) != 4:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        user_x = float(argv[1])
        user_y = float(argv[2])
    except ValueError:
        print("Error: user coordinates must be numbers", file=sys.stderr)
        return 2
    url = argv[3]

    try:
        shops = load_shops(url)
    except MalformedShopDataError as exc:
        print(f"Error: malformed shop data: {exc}", file=sys.stderr)
        return 1
    except (URLError, OSError) as exc:
        print(f"Error: could not read shop data from {url}: {exc}", file=sys.stderr)
        return 1

    # Format output as required: `Name,distance` with 4 decimal places.
    # The `:.4f` format spec rounds half-to-even (IEEE 754 default).
    for shop, distance in closest_shops(shops, user_x, user_y, limit=3):
        print(f"{shop.name},{distance:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
