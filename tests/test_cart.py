from decimal import Decimal

from pricing.cart import Line, subtotal, total


def test_subtotal_adds_lines() -> None:
    lines = [Line("a", Decimal("2.50"), 2), Line("b", Decimal("1.00"), 3)]
    assert subtotal(lines) == Decimal("8.00")


def test_total_applies_discount_then_tax() -> None:
    lines = [Line("a", Decimal("100.00"), 1)]
    assert total(lines, discount_percent=10) == Decimal("97.20")
