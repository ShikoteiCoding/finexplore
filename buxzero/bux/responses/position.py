from typing import Any

from .price import Price
from .response import Response

import pandas as pd


class Positions(list):
    """
    Position list wrapper for batch manipulation
    """

    def to_pandas(self) -> pd.DataFrame:
        records = [
            {
                "id": item.id,
                "name": item.name,
                "country_code": item.country_code,
                "type": item.type,
                "quantity": item.quantity,
                **item.offer.to_dict(prefix="offer"),
                **item.average_purchase_price.to_dict(prefix="average_purchase_price"),
            }
            for item in self
        ]

        return pd.DataFrame().from_records(records)


class Position(Response):
    @property
    def _pos(self) -> dict[str, Any]:
        return self["position"]

    @property
    def id(self) -> str:
        return self["security"]["id"]

    @property
    def name(self) -> str:
        return self["security"]["name"]

    @property
    def country_code(self) -> str | None:
        return self["security"].get("countryCode")

    @property
    def offer(self) -> Price:
        return Price(self["security"]["offer"])

    @property
    def closing_bid(self) -> Price | None:
        if "closingBid" not in self["security"]:
            return None
        return Price(self["security"]["closingBid"])

    @property
    def bid(self) -> Price | None:
        if "bid" not in self["security"]:
            return None
        return Price(self["security"]["bid"])

    @property
    def type(self) -> str:
        return self["security"]["securityType"]

    @property
    def buy_amount(self) -> Price:
        return Price(self._pos["allTimeChanges"]["buyAmount"])

    @property
    def cash_change(self) -> Price:
        return Price(self._pos["allTimeChanges"]["cashChange"])

    @property
    def sell_amount(self) -> Price:
        return Price(self._pos["allTimeChanges"]["sellAmount"])

    @property
    def average_purchase_price(self) -> Price:
        return Price(self._pos["averagePurchasePrice"])

    @property
    def average_purchase_price_in_user_currency(self) -> Price:
        return Price(self._pos["averagePurchasePriceInUserCurrency"])

    @property
    def investment_amount(self) -> Price:
        return Price(self._pos["investmentAmount"])

    @property
    def previous_closing_amount(self) -> Price:
        return Price(self._pos["previousClosingAmount"])

    @property
    def quantity(self) -> float:
        return float(self._pos["quantity"])

    @property
    def today_quantity(self) -> int:
        return int(self._pos["todayPerformance"]["quantity"])

    @property
    def change_amount(self) -> Price:
        return Price(self._pos["todayPerformance"]["changeAmount"])

    @property
    def intra_day_trades_amount(self) -> Price:
        return Price(self._pos["todayPerformance"]["intraDayTradesAmount"])
