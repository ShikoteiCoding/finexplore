##
#   Fake API connection to make strategy pattern simulation
#   Modify to make it work
##
from dataclasses import KW_ONLY, dataclass, field
from typing import Optional
from alpaca_trade_api.common import URL
from alpaca_trade_api.rest import REST

##
#   Errors
##
class BrokerConnectionError(Exception):
    pass

# TODO : Broker Trade Class, Orders Class (those are just structures to hold needed data)
# Broker should encapsulate : Trades, Orders, Position ?
# Might be overkill because we would need to find a really generic solution between brokers.
# Duck typing might be the key here to avoid fake inheritance.
@dataclass
class Position:
    """
    Position class. Holds data necessary for positionned money.
    To be passed to the strategy as a lighter version of Broker.
    """

    _in_position:   bool    = field(init=True, repr=True)
    _size:          int     = field(init=True, repr=True)
    _cash_amount:   float   = field(init=True, repr=True)
    _equity:        float   = field(init=True, repr=True)

    @property
    def in_position(self) -> bool:
        return self._in_position

    @in_position.setter
    def in_position(self, val: bool) -> None:
        self._in_position = val

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, val: int) -> None:
        self._size = val

    @property
    def equity(self) -> float:
        return self._equity

    @equity.setter
    def equity(self, val: float) -> None:
        self._equity = val

    @property
    def cash_amount(self) -> float:
        return self._cash_amount

    @cash_amount.setter
    def cash_amount(self, val: float) -> None:
        self._cash_amount = val
    
    @staticmethod
    def load_positions(file_path: str) -> list: # type: ignore
        """ Theortically, we can have ongoing orders before debuting a strategy (for example comming from another strategy). """
        pass

@dataclass
class Order:
    """
    Order class. To keep track of any information relatively of an order.
    An order is not necessarly successful. Once it is, it becomes a trade.
    """

    # TODO: For now, because orders / trades are affecting the data contained in the broker
    # We need to keep the reference in each object ...
    # This is a real bad implementation because it is not really a tree data structure
    # This might be addressed more elegantly with functionnal programming
    # Giving the order a broker partial method (to self) to affect the broker class
    # I can't do it right now because I stil can't define properly
    # What will / might be modified. So let's keep the reference for now but needed for future improvment fs.
    _broker: 'Broker' = field(init=True, repr=True)

    _symbol: str = field(init=True,  repr=True)
    _size:   int = field(init=True,  repr=True)
    _type:   str = field(init=True,  repr=True)

    _: KW_ONLY
    _limit_price: Optional[float] = field(init=True, repr=True, default=None)
    _stop_price:  Optional[float] = field(init=True, repr=True, default=None)
    _sl_price:    Optional[float] = field(init=True, repr=True, default=None)
    _tp_price:    Optional[float] = field(init=True, repr=True, default=None)

    _long: bool  = field(init=False, repr=True)
    _short: bool = field(init=False, repr=True)

    def __post_init__(self):
        self._long = self._size > 0
        self._short = self._size < 0

    @property
    def broker(self) -> 'Broker':
        return self._broker
    @property
    def symbol(self) -> str:
        return self._symbol
    @property
    def size(self) -> int:
        return self._size
    @property
    def type(self) -> str:
        return self._type
    @property
    def is_long(self) -> bool:
        return self._long
    @property
    def is_short(self) -> bool:
        return self._short

    def cancel(self) -> None:
        """ Cancel an order. """
        raise NotImplementedError()
        
    @staticmethod
    def load_orders(file_path: str) -> list: # type: ignore
        """
        Theortically, we can have ongoing orders before debuting a strategy.
        For instance comming from another strategy.
        """
        pass

@dataclass
class Trade:
    """ Trade class. To keep track of closed orders. """

    # TODO: For now, because orders / trades are affecting the data contained in the broker
    # We need to keep the reference in each object ...
    # This is a real bad implementation because it is not really a tree data structure
    # This might be addressed more elegantly with functionnal programming
    # Giving the order a broker partial method (to self) to affect the broker class
    # I can't do it right now because I stil can't define properly
    # What will / might be modified. So let's keep the reference for now but needed for future improvment fs.
    _broker: 'Broker' = field(init=True, repr=True)

    _symbol: str = field(init=True,  repr=True)
    _size:   int = field(init=True,  repr=True)
    _type:   str = field(init=True,  repr=True)

    _: KW_ONLY
    _entry_price:   float           = field(init=True, repr=True)
    _entry_time:    str             = field(init=True, repr=True)
    _exit_price:    Optional[float] = field(init=True, repr=False, default=None)
    _exit_time:     Optional[str]   = field(init=True, repr=False, default=None)

    def __post_init__(self):
        self.display_init()
        self._is_long = self._size > 0
        self._is_short = self._size < 0

    @property
    def broker(self) -> 'Broker':
        return self._broker
    @property
    def symbol(self) -> str:
        return self._symbol
    @property
    def size(self) -> int:
        return self._size
    @property
    def type(self) -> str:
        return self._type
    @property
    def entry_price(self) -> float:
        return self._entry_price
    @property
    def exit_price(self) -> Optional[float]:
        return self._exit_price
    @property
    def entry_time(self) -> str:
        return self._entry_time
    @property
    def exit_time(self) -> Optional[str]:
        return self._exit_time
    @property
    def is_long(self) -> bool:
        return self._is_long
    @property
    def is_short(self) -> bool:
        return self._is_short
    @property
    def pl(self) -> int:
        return 0

    def display_init(self) -> None:
        order_size = "Long" if self._size > 0 else "Short"
        print(f"{self._entry_time}\n{order_size} Trade of size: {self._size} has been approved for symbol: {self._symbol}")

@dataclass
class Broker:
    """
    Broker class. To encapsulate APIs or Websockets protocols. 
    Should be using duck typing through typing.Protocol.
    """

    _cash_amount: float     = field(init=True, repr=True, default=1000)

    _position: Position     = field(init=False, repr=True) # Default empty if no existing position pre deployment
    _orders:   list[Order]  = field(init=False, repr=True, default_factory=list)    # Default empty if no existing orders pre deployment
    _trades:   list[Trade]  = field(init=False, repr=True, default_factory=list)    # Always empty : don't track pre deployment trades (no sense)

    def __post_init__(self):
        self._position = Position(False, 0, self._cash_amount, self._cash_amount)

    @property
    def in_position(self) -> bool:
        """ Boolean to use in strategies. """
        return self._position.in_position

    @property
    def cash_amount(self) -> float:
        return self._cash_amount

    @property
    def equity(self) -> float:
        return self._cash_amount + sum(trade.pl for trade in self._trades)

    @property
    def position(self) -> Optional[Position]:
        return self._position
    
    @property
    def orders(self) -> list[Order]:
        return self._orders
    
    @property
    def trades(self) -> list[Trade]:
        return self._trades

    def max_long(self, price: float) -> int:
        """ Returns the maximum positive quantity available to buy. """
        return int(self._cash_amount // price)

    def max_short(self) -> int:
        """ Returns the maximum positive quantity available to sell. """
        return sum(trade.size for trade in self.trades)

    def sell(self, symbol: str, size: int, price: float, date: str):
        # At this step we don't know if the order is successful or not
        self.orders.append(self.create_order(symbol, size, price, date))

    def buy(self, symbol: str, size: int, price: float, date: str):
        # At this step we don't know if the order is successful or not
        self.orders.append(self.create_order(symbol, size, price, date))

    def create_order(self, symbol: str, size: int, price: float, date: str) -> Order:
        return Order(
            _broker=self,
            _symbol=symbol,
            _size=size,
            _type="ioc"
        )
    
    def create_trade(self, symbol: str, size: int, price: float, entry_date: str) -> Trade:
        return Trade(
            _broker=self,
            _symbol=symbol,
            _size=size,
            _type="ioc",
            _entry_price=price,
            _entry_time=entry_date
        )

    def process_orders(self, symbol: str, current_price: float, current_time: str):
        """
        Process the orders to update internal data.
        Are queing two type of oders:
            - Orders not yet successful
            - Orders with limit (stop loss or take profit)
        """
        for order in self.orders:

            # First case: normal order
            if order.symbol == symbol and order.type=="ioc":
                self.record_trade(self.create_trade(symbol, order.size, current_price, current_time))

            # TODO: Handle sl and tp trades. Be careful. They are not necessarly closed after being issued.
            self.orders.remove(order)

        self.update_position(current_price)

    def record_trade(self, trade: Trade) -> None:
        """
        When a trade is created some actions are to be handled.
        Deal with those various actions here.
        """
        self._cash_amount -= (trade.size * trade.entry_price)   # Update available cash
        self.trades.append(trade)

    def update_position(self, current_price: float) -> None:
        total_size = sum(trade.size for trade in self._trades)

        self._position.in_position = total_size > 0
        self._position.size = total_size
        self._position.cash_amount = self._cash_amount
        self._position.equity = self._position._cash_amount + current_price * self._position.size

@dataclass
class BackTestBroker:
    """ Backtesting Broker to log transactions. """
    
    transaction_history: list[int]

    def buy(self, symbol: str, amount: int) -> None:
        """Simulate buying an amount of a given symbol at the current price."""
        print(f"Buying amount {amount} in market {symbol}.")

    def sell(self, symbol: str, amount: int) -> None:
        """Simulate selling an amount of a given symbol at the current price."""
        print(f"Selling amount {amount} in market {symbol}.")

    def get_transactions(self) -> list[int]:
        """ Get Transaction History. """
        return self.transaction_history

@dataclass
class AlpacaBroker:
    """ Alpaca API Connector. Behavioral class. """
    
    key_id: str
    secret_key: str
    base_url: str

    def connect(self) -> None:
        """ Connect to Alpaca API. Unfortunately, no response at this step. """
        self.connection = REST(
            key_id = self.key_id,
            secret_key = self.secret_key,
            base_url = URL(self.base_url),
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

    def get_market_data(self, symbol: str) -> None: 
        pass

class YFinance:
    """ Get Market Data from Yahoo Finance. """

    def get_market_data(self, symbol: str) -> None:
        pass