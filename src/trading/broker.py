##
#   Fake API connection to make strategy pattern simulation
#   Modify to make it work
##
from dataclasses import KW_ONLY, dataclass, field
from typing import Optional, Union
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

    _in_position:     bool    = field(init=True, repr=True)
    _size:            int     = field(init=True, repr=True)
    _cash_amount:     float   = field(init=True, repr=True)
    _equity:          float   = field(init=True, repr=True)
    _position_amount: float   = field(init=True, repr=False)

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
    @property
    def position_amount(self) -> float:
        return self._position_amount
    @position_amount.setter
    def position_amount(self, val: float) -> None:
        self._position_amount = val
    
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

    _symbol:        str     = field(init=True,  repr=True)
    _size:          int     = field(init=True,  repr=True)
    _type:          str     = field(init=True,  repr=True)
    _time:          str     = field(init=True,  repr=True)
    _cash_reserved: float   = field(init=True, repr=True)   # TODO: Stock cash reservation somewhere else? Seems weak here

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
    @property
    def cash_reserved(self) -> float:
        return self._cash_reserved

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
    _broker: 'Broker' = field(init=True, repr=False)

    _symbol: str = field(init=True,  repr=True)
    _size:   int = field(init=True,  repr=True)
    _type:   str = field(init=True,  repr=True)

    _: KW_ONLY
    _entry_price:   float           = field(init=True, repr=True)
    _entry_time:    str             = field(init=True, repr=True)
    _debug: bool                    = field(init=True, repr=False, default=True)

    def __post_init__(self):
        if self._debug: self.display_init()
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
    def entry_time(self) -> str:
        return self._entry_time
    @property
    def is_long(self) -> bool:
        return self._is_long
    @property
    def is_short(self) -> bool:
        return self._is_short

    def display_init(self) -> None:
        order_size = "Long" if self._size > 0 else "Short"
        print(f"{self._entry_time}\n{order_size} Trade of size: {self._size} has been approved for symbol: {self._symbol}")



class Equity(int):
    MAX_LONG    = 1
    MAX_SHORT   = -1

@dataclass
class Broker:
    """
    Broker class. To encapsulate APIs or Websockets protocols. 
    Should be using duck typing through typing.Protocol.
    """

    _cash_amount: float     = field(init=True, repr=True, default=1000)

    _:KW_ONLY
    _debug: bool = field(init=True, repr=False, default=True)

    _position: Position     = field(init=False, repr=True) # Default empty if no existing position pre deployment
    _orders:   list[Order]  = field(init=False, repr=True, default_factory=list)    # Default empty if no existing orders pre deployment
    _trades:   list[Trade]  = field(init=False, repr=True, default_factory=list)    # Always empty : don't track pre deployment trades (no sense)
    _cover_rate: int        = field(init=False, repr=True, default=0)
    _commision_rate: float  = field(init=False, repr=True, default=0.0)
    
    def __post_init__(self):
        self._position = Position(False, 0, self._cash_amount, self._cash_amount, 0)

    @property
    def in_position(self) -> bool:
        """ Boolean to use in strategies. """
        return self._position.in_position
    @property
    def cash_amount(self) -> float:
        return self._cash_amount
    @property
    def position(self) -> Position:
        return self._position
    @property
    def orders(self) -> list[Order]:
        return self._orders
    @property
    def trades(self) -> list[Trade]:
        return self._trades
    @property
    def equity(self) -> float:
        return self.position.equity
    @property
    def cash_reserved(self) -> float:
        return sum(order._cash_reserved for order in self.orders)
    @property
    def commision_rate(self) -> float:
        return self._commision_rate
    @commision_rate.setter
    def commision_rate(self, val: float) -> None:
        self._commision_rate = val

    def max_long(self, price: float) -> int:
        """ Returns the maximum positive quantity available to buy. """
        return int(self._cash_amount // price)

    def max_short(self) -> int:
        """ Returns the maximum positive quantity available to sell. """
        return self.position.size

    def sell(self, symbol: str, size: int, price: float, time: str):
        # At this step we don't know if the order is successful or not
        if size == Equity.MAX_SHORT:
            self.orders.append(self.create_order(symbol, - self.max_short(), price, time))
        else:
            self.orders.append(self.create_order(symbol, - size, price, time))

    def buy(self, symbol: str, size: int, price: float, time: str):
        # At this step we don't know if the order is successful or not
        if size == Equity.MAX_LONG:
            self.orders.append(self.create_order(symbol, self.max_long(price), price, time))
        else:
            self.orders.append(self.create_order(symbol, size, price, time))

    def reserve_cash(self, amount: float) -> None:
        """ When an order is created, the amount is unavailable and bound to the successfullness of the order. """
        self._cash_amount -= (amount * (1 + self._cover_rate))

    def create_order(self, symbol: str, size: int, price: float, time: str) -> Order:
        self.reserve_cash(size * price if size > 0 else 0)
        return Order(
            _broker=self,
            _symbol=symbol,
            _size=size,
            _type="ioc",
            _time=time,
            _cash_reserved= size * price if size > 0 else 0
        )
    
    def create_trade(self, order: Order, price: float, entry_time: str) -> tuple[Order, Trade]:
        """ Create a trade from an existing order. """
        return order, Trade(
            _broker=self,
            _symbol=order.symbol,
            _size=order.size,
            _type=order.type,
            _entry_price=price,
            _entry_time=entry_time,
            _debug=self._debug
        )

    def process_orders(self, symbol: str, current_price: float, current_time: str) -> dict[str, int]:
        """
        Process the orders to update internal data.
        Are queing two type of oders:
            - Orders not yet successful
            - Orders with limit (stop loss or take profit)
        Not sure of this method if it reflects truly the behavior of the API.
        Might be more like : create order -> create trade
        """
        sum_long = 0
        sum_short = 0

        for order in self.orders:

            # First case: normal order
            if order.symbol == symbol and order.type=="ioc":
                trade_size = self.record_trade(*self.create_trade(order, current_price, current_time))
                if (trade_size > 0) : sum_long += trade_size
                else: sum_short += trade_size

            # TODO: Handle sl and tp trades. Be careful. They are not necessarly closed after being issued.
            self.orders.remove(order)

        self.update_position(current_price)

        return {"enter": sum_long, "exit": sum_short}

    def record_trade(self, order: Order, trade: Trade) -> int:
        """
        When a trade is created some actions are to be handled.
        Deal with those various actions here.
        """
        if order.is_long:
            left_over = order.cash_reserved - (trade.size * trade.entry_price) # Reserved amount is always higher
            self._cash_amount = self._cash_amount + left_over       # Add the left over
        if order.is_short:
            self._cash_amount -= (trade.size * trade.entry_price)   # Add to cash amount sold

        # Deal with IOC partial orders here ?
        # remove max trade.size for available cash amount should simulate IOC.
        self.trades.append(trade)
        return trade.size

    def update_position(self, current_price: float) -> None:
        """
        This method allows to systematically keep position up to date.
        """
        # Sum of previous trade size is the current held size
        current_size = sum(trade.size for trade in self._trades)

        # In position if at least one symbol hold
        self._position.in_position = current_size > 0
        self._position.size = current_size
        self._position.cash_amount = self._cash_amount
        self._position.equity = self._cash_amount + current_price * current_size
        self._position.position_amount = current_price * current_size

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