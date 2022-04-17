from dataclasses import KW_ONLY, dataclass, field
from functools import partial, update_wrapper
from re import S
from typing import Callable, Dict, NoReturn, Optional, TypeAlias, Union, cast

import numpy as np
import pandas as pd

##
#   Utilities
##



##
#   Global variables
##
DATA_PATH = "../../data/companies_stock/"
CSV_EXT = ".csv"

##
#   Type declarations
##

# Errors
class DatasetNotFound(Exception):
    pass
class AlreadyInPosition(Exception):
    pass
class NotInPosition(Exception):
    pass
class NotAlterableDataset(Exception):
    pass

##
#   Classes for data management
##
    
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
    _entry_price:   Optional[float]  = field(init=True,  repr=True, default=None)
    _entry_date:    Optional[str]    = field(init=True,  repr=True, default=None)
    _exit_price:    Optional[float]  = field(init=True, repr=False, default=None)
    _exit_date:     Optional[str]    = field(init=True, repr=False, default=None)

    _long: bool  = field(init=False, repr=True)
    _short: bool = field(init=False, repr=True)

    def __post_init__(self):
        self.display_init()
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
    def entry_price(self) -> Optional[float]:
        return self._entry_price
    
    @property
    def exit_price(self) -> Optional[float]:
        return self._exit_price

    @property
    def entry_date(self) -> Optional[str]:
        return self._entry_date

    @property
    def exit_date(self) -> Optional[str]:
        return self._exit_date

    @property
    def long(self) -> bool:
        return self.long

    @property
    def short(self) -> bool:
        return self.short

    def display_init(self) -> None:
        order_size = "Long" if self._size > 0 else "Short"
        print(f"{self._entry_date}\n{order_size} Order of size: {self._size} created for symbol {self._symbol}")
    
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

class Array(np.ndarray):
    """
    Numpy ndarray extension for performances over pandas.
    Allows Talib functions without to convert each call
    """
    def __new__(cls, array, *, name=None, **kwargs):
        obj = np.asarray(array).view(cls)
        obj.name = name or array.name
        obj._opts = kwargs
        return obj

    def __array_finalize__(self, obj):
        if obj is not None:
            self.name = getattr(obj, 'name', '')
            self._opts = getattr(obj, '_opts', {})

    # Make sure properties name and _opts are carried over
    def __reduce__(self):
        value = super().__reduce__()
        return value[:2] + (value[2] + (self.__dict__,),) #type: ignore

    def __setstate__(self, state):
        self.__dict__.update(state[-1])
        super().__setstate__(state[:-1])

    def __bool__(self):
        try:
            return bool(self[-1])
        except IndexError:
            return super().__bool__()

    def __float__(self):
        try:
            return float(self[-1])
        except IndexError:
            return super().__float__()

    def __repr__(self):
        return f"Array(name={self.name}, length={len(self)})"
    
    def to_pandas(self) -> pd.Series:
        values = np.atleast_2d(self)
        index = self._opts['index'][:values.shape[1]]
        return pd.Series(values[0], index=index, name=self.name)

@dataclass
class Data:
    """ Data class to hold and interact with data efficiently through numpy arrays. """

    _df:        pd.DataFrame        = field(init=True,  repr=True,  default = pd.DataFrame())
    __len:      int                 = field(init=False, repr=False, default = 0)
    __index:    int                 = field(init=False, repr=False, default = 0)
    __cache:    Dict[str, Array]    = field(init=False, repr=False, default_factory=dict)
    __arrays:   Dict[str, Array]    = field(init=False, repr=True,  default_factory=dict)

    def __post_init__(self):
        self.__index = len(self._df)
        self.__len = len(self._df)

        index = self._df.index.copy()

        self.__arrays = { str(col).strip(" ") : Array(arr, index=index) for col, arr in self._df.items() }
        self.__arrays['_index'] = Array(index, index=index)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def len(self) -> int:
        return self.__len

    @property
    def columns(self) -> list:
        return list(self.__arrays.keys())

    @property
    def i(self) -> int:
        """
        Maximum slice value to return arrays as follows: array[:i].
        Only used for iterative exposure of a fully known dataset.
        """
        return self.__index

    @property
    def index(self) -> Array:
        return self.__get_array("_index")
    
    @i.setter
    def i(self, i):
        if i == 0:
            raise IndexError("Index should be greater than 0. Need at least a len 2 array.")
        if i > self.__len:
            raise IndexError("Index can't be greater than the maximum number of data.")
        self.__cache.clear()
        self.__index = i

    def __getitem__(self, key: str) -> Array:
        return self.__get_array(key)

    def __getattr__(self, __name: str) -> Array:
        try:
            return self.__get_array(__name)
        except KeyError:
            raise AttributeError(f"Attribute {__name} is not a known column.")

    def __get_array(self, __name: str) -> Array:
        arr = self.__cache.get(__name)
        if arr is None:
            arr = self.__cache[__name] = cast(Array, self.__arrays[__name][:self.__index])
        return arr

    def add_empty_array(self, __name: str) -> None:
        self.__arrays[__name] = Array(np.tile(np.nan, self.__len), name=__name)

    def to_pandas(self) -> pd.DataFrame:
        return self._df

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
            _type="test",
            _entry_price=price,
            _entry_date=date
        )
    
    def create_trade(self, symbol: str, size: int, price: float, entry_date: str) -> Trade:
        return Trade(
            _broker=self,
            _symbol=symbol,
            _size=size,
            _type="test",
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
            if order.symbol == symbol and order.entry_price == current_price:
                self.record_trade(self.create_trade(symbol, order.size, current_price, current_time))

            # Not necessarly true for sl and tp trades
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


# Reader Callable Type
DatasetReaderCallable: TypeAlias = Callable[[], Data]

##
#   Reader Function
##
def read_stock(stock_name: str,  _from: str = "", _to: str = "", _field: str = "") -> Data:
    """ Read csv stock. Reading logic goes here """

    try:
        df = pd.read_csv(DATA_PATH + stock_name + CSV_EXT)
    except FileNotFoundError as error: 
        raise DatasetNotFound(f"Dataset not found, please download your stock data: {stock_name}", error)

    df.index = df.Date

    if not _from and not _to:
        return  Data(df)

    if not _to:
        return Data(pd.DataFrame(df[(df.Date > _from)]))

    return Data(pd.DataFrame(df[(df.Date > _from) & (df.Date <= _to)]))

##
#   Implements a stock function for each. We can make it dynamic later on.
#   If we bundle everything into a library, this code should not be part of it.
#   For now it kept here just to keep it organized.
##
def AAPL(_from: str = "", _to: str = "") -> Data:
    return read_stock("AAPL", _from, _to)

def IBM(_from: str = "", _to: str = "") -> Data:
    return read_stock("IBM", _from, _to)

def MSFT(_from: str = "", _to: str = "") -> Data:
    return read_stock("MSFT", _from, _to)

##
#   Utils function
##

def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func
    
def get_function_name(func: Callable) -> str:
    return func.__name__
