"""Unit tests for the Shop domain object.

These tests are pure (no I/O, no mocks) because Shop itself is pure.
"""
from coffee_finder.shop import Shop


def test_distance_to_same_point_is_zero():
    # Sanity check: distance from a point to itself must be exactly 0.
    # This catches sign errors in the distance formula.
    s = Shop("A", 1.0, 2.0)
    assert s.distance_to(1.0, 2.0) == 0.0


def test_distance_euclidean():
    # 3-4-5 Pythagorean triple: distance from (3,4) to (0,0) is exactly 5.
    # Using integer-result coordinates avoids float comparison issues.
    s = Shop("A", 3.0, 4.0)
    assert s.distance_to(0.0, 0.0) == 5.0
