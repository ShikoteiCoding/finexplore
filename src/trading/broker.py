##
#   Fake API connection to make strategy pattern simulation
#   Modify to make it work
##

import functools
import alpaca_trade_api as tradeapi
from data.fake_price_data import CRYPTO_DATA
import logging

from typing import Protocol

class BrokerConnectionError(Exception):
    pass

class Broker(Protocol):
    """ Broker protocol that declares connection and trading related methods. """
    def connect(self) -> None:
        ...
    
    def check_connection(self) -> None:
        ...
    
    def buy(self, symbol: str, amount: int) -> None:
        ...

    def sell(self, sumbol: str, amount: int) -> None:
        ...

class MarketData(Protocol):
    """ Market data protocol that declares method to fetch data. """
    def get_market_data(self, symbol: str) -> list[int]:
        ...


class DemoBroker:
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


class AlpacaBroker:
    """ Alpaca API Connector. Behavioral class. """

    def connect(self) -> None:
        self.connection = tradeapi.REST()
        logging.info("Successfull connection")
    
    def check_connection(self) -> None:
        res = self.connection.get_account()
        if not res:
            raise BrokerConnectionError("Not able to connect")

    def buy(self) -> None:
        pass

    def sell(self) -> None:
        pass

    def get_market_data(self) -> None: 
        pass