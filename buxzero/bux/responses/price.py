from decimal import Decimal
from typing import Any

from .response import Response


class Price(Response):
    @property
    def amount(self) -> Decimal:
        return Decimal(self["amount"])

    @property
    def currency(self) -> str:
        return self["currency"]

    @property
    def decimals(self) -> int:
        return self["decimals"]

    def to_dict(self, prefix: str = "", prefix_sep=".") -> dict[str, Any]:
        return {
            (prefix + prefix_sep if prefix else "") + "amount": self.amount,
            (prefix + prefix_sep if prefix else "") + "currency": self.currency,
            (prefix + prefix_sep if prefix else "") + "decimals": self.decimals,
        }

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"

    def __format__(self, spec: str) -> str:
        amount = format(self.amount, spec)
        return f"{amount} {self.currency}"

    def __eq__(self, other: 'Price') -> bool:
        if not isinstance(other, Price): return False
        return self.amount == other.amount and self.currency == other.currency

    def __ge__(self, other: 'Price') -> bool:
        return self.currency == other.currency and self.amount >= other.amount

    def __gt__(self, other: 'Price') -> bool:
        return self.currency == other.currency and self.amount > other.amount

    def __le__(self, other: 'Price') -> bool:
        return self.currency == other.currency and self.amount <= other.amount

    def __lt__(self, other: 'Price') -> bool:
        return self.currency == other.currency and self.amount < other.amount

    def __ne__(self, other: 'Price') -> bool:
        return self.currency != other.currency or self.amount != other.amount
