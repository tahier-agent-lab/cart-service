"""Cart pricing: the total of a cart's lines, with an optional discount and tax."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

TAX_RATE = Decimal("0.08")


@dataclass(frozen=True)
class Line:
    sku: str
    unit_price: Decimal
    quantity: int


def subtotal(lines: list[Line]) -> Decimal:
    return sum((line.unit_price * line.quantity for line in lines), Decimal("0"))


def total(lines: list[Line], discount_percent: int = 0) -> Decimal:
    if not 0 <= discount_percent < 100:
        raise ValueError(
            f"discount_percent must be between 0 and 100 (exclusive), got {discount_percent}"
        )
    amount = subtotal(lines) * (Decimal(100 - discount_percent) / 100)
    with_tax = amount * (1 + TAX_RATE)
    return with_tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
