##
#   Layout of Functionnal Strategy Pattern
##
import statistics
from typing import Callable, Protocol
from dataclasses import dataclass
from functools import partial

from data.fake_price_data import CRYPTO_DATA

##
#   This file contains a full simple framework which is used has a simple template to improve
##

# Rule Function Signature
TradingStrategyRule = Callable[[list[int]], bool]

##
#   Errors
##
class BrokerConnectionError(Exception):
    pass

def should_buy_avg(prices: list[int], window_size: int) -> bool:
    # Make a decision based on 
    list_window = prices[-window_size:]
    return prices[-1] < statistics.mean(list_window)


def should_sell_avg(prices: list[int], window_size: int) -> bool:
    list_window = prices[-window_size:]
    return prices[-1] > statistics.mean(list_window)


def should_buy_minmax(prices: list[int], max_price: int) -> bool:
    # buy if it's below the max price
    return prices[-1] < max_price


def should_sell_minmax(prices: list[int], min_price: int) -> bool:
    # sell if it's above the min price
    return prices[-1] > min_price

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

    def sell(self, symbol: str, amount: int) -> None:
        ...

class MarketData(Protocol):
    """ Market data protocol that declares method to fetch data. """
    def get_market_data(self, symbol: str) -> list[int]:
        ...
##
#   Actual Brokers
##
class DemoBroker:
    """ Demo Broker. """
    def __init__(self) -> None:
        self.connected = False
    
    def connect(self) -> None:
        """Connect to the exchange."""
        print("Connecting to Crypto exchange...")
        self.connected = True

    def check_connection(self) -> None:
        """Check if the exchange is connected."""
        if not self.connected:
            raise BrokerConnectionError("Not able to connect")

    def get_market_data(self, symbol: str) -> list[int]:
        """Return fake market price data for a given market symbol."""
        self.check_connection()
        return CRYPTO_DATA[symbol]

    def buy(self, symbol: str, amount: int) -> None:
        """Simulate buying an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Buying amount {amount} in market {symbol}.")

    def sell(self, symbol: str, amount: int) -> None:
        """Simulate selling an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Selling amount {amount} in market {symbol}.")

@dataclass
class DemoRuleBasedStrategy:
    """Trading bot that connects to a crypto broker and performs trades."""

    broker: Broker
    automate: Automate
    marketdata: MarketData
    buy_strategy: TradingStrategyRule
    sell_strategy: TradingStrategyRule

    def run(self, symbol: str) -> None:
        prices = self.marketdata.get_market_data(symbol)
        if self.buy_strategy(prices):
            self.automate.buy(symbol, 10)
        elif self.sell_strategy(prices):
            self.automate.sell(symbol, 10)
        else:
            print(f"No action needed for {symbol}.")

def example() -> None:

    # Connection to broker
    demo_broker = DemoBroker()
    demo_broker.connect()

    # Strategy values
    buy_strategy = partial(should_buy_avg, window_size=30)
    sell_strategy = partial(should_sell_minmax, min_price=38_000)

    strategy = DemoRuleBasedStrategy(
        broker = demo_broker,
        automate = demo_broker,
        marketdata = demo_broker,
        buy_strategy = buy_strategy,
        sell_strategy = sell_strategy)
    strategy.run("BTC/USD")

if __name__ == '__main__':
    example()