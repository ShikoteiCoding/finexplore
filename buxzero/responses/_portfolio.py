from ._response import Response
from ._position import Position
from ._price import Price

from itertools import chain

from typing import Any

class PortfolioPosition(Position):
    """
    Properties related to portfolio.
    """
    @property
    def _pos(self) -> dict[str, Any]:
        return self['position']

    @property
    def id(self) -> str:
        return self['security']['id']

    @property
    def name(self) -> str:
        return self['security']['name']

    @property
    def country_code(self) -> str | None:
        return self['security'].get('countryCode')

    @property
    def offer(self) -> Price:
        return Price(self['security']['offer'])

    @property
    def closing_bid(self) -> Price | None:
        if 'closingBid' not in self['security']:
            return None
        return Price(self['security']['closingBid'])

    @property
    def bid(self) -> Price | None:
        if 'bid' not in self['security']:
            return None
        return Price(self['security']['bid'])

    @property
    def type(self) -> str:
        return self['security']['securityType']


class Portfolio(Response):
    @property
    def account_value(self) -> Price:
        return Price(self['accountValue'])

    @property
    def all_time_deposit_and_withdraws(self) -> Price:
        return Price(self['allTimeDepositAndWithdraws'])

    @property
    def all_time_trades_amount(self) -> Price:
        return Price(self['allTimeTradesAmount'])

    @property
    def available_cash(self) -> Price:
        return Price(self['availableCash'])

    @property
    def cash_balance(self) -> Price:
        return Price(self['cashBalance'])

    @property
    def intra_day_trades_amount(self) -> Price:
        return Price(self['intraDayTradesAmount'])

    @property
    def invested_amount(self) -> Price:
        return Price(self['investedAmount'])

    @property
    def previous_closing_amount(self) -> Price:
        return Price(self['previousClosingAmount'])

    @property
    def reserved_cash(self) -> Price:
        return Price(self['reservedCash'])

    @property
    def markets_open(self) -> bool:
        return self['marketsOpen']

    @property
    def positions(self) -> list[PortfolioPosition]:
        poss = chain(
            self['positions']['EQTY'],
            self['positions']['ETF'],
        )
        return [PortfolioPosition(p) for p in poss]