"""Unit tests for the closest-shops business logic."""
from coffee_finder.finder import closest_shops
from coffee_finder.shop import Shop


def test_returns_sorted_top_n():
    # Input is intentionally unsorted and has more items than `limit`.
    # The function must both sort by distance AND truncate to `limit`.
    shops = [
        Shop("Far", 10.0, 10.0),
        Shop("Near", 1.0, 1.0),
        Shop("Mid", 5.0, 5.0),
        Shop("Farther", 20.0, 20.0),
    ]
    result = closest_shops(shops, 0.0, 0.0, limit=3)
    names = [s.name for s, _ in result]
    assert names == ["Near", "Mid", "Far"]


def test_example_from_challenge():
    # Acceptance test: reproduces the exact example from the challenge
    # description. If this passes, the business logic meets requirements.
    shops = [
        Shop("Starbucks Seattle", -122.3160, 47.5809),
        Shop("Starbucks Seattle2", -122.3340, 47.6160),
        Shop("Starbucks SF", -122.4194, 37.7749),
    ]
    result = closest_shops(shops, -122.4, 47.6, limit=3)
    names = [s.name for s, _ in result]
    assert names[0] == "Starbucks Seattle2"
    assert names[1] == "Starbucks Seattle"
    assert names[2] == "Starbucks SF"
