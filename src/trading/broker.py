##
#   Fake API connection to make strategy pattern simulation
#   Modify to make it work
##

import functools
import alpaca_trade_api as tradeapi
from data.fake_price_data import CRYPTO_DATA

##
#   Errors
##
class BrokerConnectionError(Exception):
    pass


##
#   Actual Brokers
##
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

    def __init__(self, key_id: str, secret_key: str, base_url: str):
        self.key_id = key_id
        self.secret_key = secret_key
        self.base_url = base_url

    def connect(self) -> None:
        """ Connect to Alpaca API. Unfortunately, no response at this step. """
        self.connection = tradeapi.REST(
            key_id = self.key_id,
            secret_key = self.secret_key,
            base_url = self.base_url,
            api_version = "v2",
            oauth = None,
            raw_data = False
        )
        print("REST API parameters are set. Check connection to verify.")
    
    def check_connection(self) -> None:
        """ Checking if connection is established by looking into account. """
        res = self.connection.get_account()
        if not res:
            raise BrokerConnectionError("Not able to connect.")
        print("Connection success.")

    def buy(self) -> None:
        pass

    def sell(self) -> None:
        pass

    def get_market_data(self) -> None: 
        pass