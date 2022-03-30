from dataclasses import dataclass

from typing import Union, Protocol

from rule import *

##
#   Listing strategies for bots.
#   1 - End of Day strategy
#   2 - Swing strategy
#   3 - Day strategy
#   4 - Trend (rule based) strategy
#   5 - Scalping strategy
#   6 - Position (long term) strategy
##

##
#   Protocols (Functional Interfaces) 
#   Ultimately not to be declared here but where it is used to avoid conflicts
##
class Broker(Protocol):
    """ Broker protocol that declares connection and trading related methods. """
    def connect(self) -> None:
        ...
    
    def check_connection(self) -> None:
        ...

class Automate(Protocol):
    """ Automate protocol that declares method for a bot to buy and sell. """
    def buy(self, symbol: str, amount: int) -> None:
        ...

    def sell(self, sumbol: str, amount: int) -> None:
        ...

class MarketData(Protocol):
    """ Market data protocol that declares method to fetch data. """
    def get_market_data(self, symbol: str) -> list[int]:
        ...

@dataclass
class DemoRuleBasedStrategy:
    """Trading bot that connects to a crypto broker and performs trades."""

    broker: Union[Broker, Automate, MarketData] # not sure about that ?
    buy_strategy: TradingStrategyRule
    sell_strategy: TradingStrategyRule

    def run(self, symbol: str) -> None:
        prices = self.broker.get_market_data(symbol)
        if self.buy_strategy(prices):
            self.broker.buy(symbol, 10)
        elif self.sell_strategy(prices):
            self.broker.sell(symbol, 10)
        else:
            print(f"No action needed for {symbol}.")