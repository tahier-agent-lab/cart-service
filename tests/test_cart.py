from decimal import Decimal

import pytest

from pricing.cart import Line, subtotal, total


def test_subtotal_adds_lines() -> None:
    lines = [Line("a", Decimal("2.50"), 2), Line("b", Decimal("1.00"), 3)]
    assert subtotal(lines) == Decimal("8.00")


def test_total_applies_discount_then_tax() -> None:
    lines = [Line("a", Decimal("100.00"), 1)]
    assert total(lines, discount_percent=10) == Decimal("97.20")


def test_subtotal_counts_every_line_beyond_max_lines() -> None:
    lines = [Line("sku", Decimal("1.00"), 1) for _ in range(25)]
    assert subtotal(lines) == Decimal("25.00")


def test_total_rejects_discount_over_100_percent() -> None:
    lines = [Line("a", Decimal("100.00"), 1)]
    with pytest.raises(ValueError):
        total(lines, discount_percent=150)


def test_total_rejects_negative_discount() -> None:
    lines = [Line("a", Decimal("100.00"), 1)]
    with pytest.raises(ValueError):
        total(lines, discount_percent=-1)


def test_total_allows_discount_of_exactly_100_percent() -> None:
    lines = [Line("a", Decimal("100.00"), 1)]
    assert total(lines, discount_percent=100) == Decimal("0.00")
