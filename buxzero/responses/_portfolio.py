from ._response import Response
from ._position import Position, Positions
from ._price import Price

from itertools import chain

import pandas as pd


class Portfolio(Response):
    @property
    def account_value(self) -> Price:
        return Price(self["accountValue"])

    @property
    def all_time_deposit_and_withdraws(self) -> Price:
        return Price(self["allTimeDepositAndWithdraws"])

    @property
    def all_time_trades_amount(self) -> Price:
        return Price(self["allTimeTradesAmount"])

    @property
    def available_cash(self) -> Price:
        return Price(self["availableCash"])

    @property
    def cash_balance(self) -> Price:
        return Price(self["cashBalance"])

    @property
    def intra_day_trades_amount(self) -> Price:
        return Price(self["intraDayTradesAmount"])

    @property
    def invested_amount(self) -> Price:
        return Price(self["investedAmount"])

    @property
    def previous_closing_amount(self) -> Price:
        return Price(self["previousClosingAmount"])

    @property
    def reserved_cash(self) -> Price:
        return Price(self["reservedCash"])

    @property
    def markets_open(self) -> bool:
        return self["marketsOpen"]

    @property
    def positions(self) -> Positions:
        poss = chain(
            self["positions"]["EQTY"],
            self["positions"]["ETF"],
        )
        return Positions([Position(p) for p in poss])
