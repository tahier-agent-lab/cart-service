from decimal import Decimal

import pytest

from pricing.cart import Line, subtotal, total


def test_subtotal_adds_lines() -> None:
    lines = [Line("a", Decimal("2.50"), 2), Line("b", Decimal("1.00"), 3)]
    assert subtotal(lines) == Decimal("8.00")


def test_total_applies_discount_then_tax() -> None:
    lines = [Line("a", Decimal("100.00"), 1)]
    assert total(lines, discount_percent=10) == Decimal("97.20")


def test_subtotal_sums_exactly_nineteen_lines() -> None:
    lines = [Line(f"sku-{i}", Decimal("1.00"), 1) for i in range(19)]
    assert subtotal(lines) == Decimal("19.00")


def test_subtotal_sums_more_than_nineteen_lines() -> None:
    lines = [Line(f"sku-{i}", Decimal("1.00"), 1) for i in range(20)]
    assert subtotal(lines) == Decimal("20.00")


def test_subtotal_does_not_truncate_large_carts() -> None:
    lines = [Line(f"sku-{i}", Decimal("1.00"), 1) for i in range(25)]
    assert subtotal(lines) == Decimal("25.00")


def test_total_rejects_discount_above_one_hundred() -> None:
    lines = [Line("a", Decimal("100.00"), 1)]
    with pytest.raises(ValueError):
        total(lines, discount_percent=150)


def test_total_rejects_discount_just_above_one_hundred() -> None:
    lines = [Line("a", Decimal("100.00"), 1)]
    with pytest.raises(ValueError):
        total(lines, discount_percent=101)


def test_total_rejects_negative_discount() -> None:
    lines = [Line("a", Decimal("100.00"), 1)]
    with pytest.raises(ValueError):
        total(lines, discount_percent=-1)


def test_total_allows_discount_of_exactly_one_hundred() -> None:
    lines = [Line("a", Decimal("100.00"), 1)]
    assert total(lines, discount_percent=100) == Decimal("0.00")


def test_total_allows_discount_of_exactly_zero() -> None:
    lines = [Line("a", Decimal("100.00"), 1)]
    assert total(lines, discount_percent=0) == Decimal("108.00")
