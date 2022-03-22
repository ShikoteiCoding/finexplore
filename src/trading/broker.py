##
#   Fake API connection to make strategy pattern simulation
#   Modify to make it work
##
import functools
from data.fake_price_data import CRYPTO_DATA

class BrokerConnectionError(Exception):
    pass

class Broker:
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