from dataclasses import KW_ONLY, dataclass, field
from functools import partial, update_wrapper
from typing import Dict, Optional, cast
import numpy as np

import pandas as pd

##
#   Utilities
##

import pandas as pd
from typing import Callable


##
#   Global variables
##
DATA_PATH = "../../data/companies_stock/"
CSV_EXT = ".csv"

##
#   Type declarations
##

# Callables
DatasetReaderCallable = Callable[[],pd.DataFrame]

# Classes
class Broker:       # type: ignore
    pass 
class Order:        # type: ignore
    pass 
class Trade:        # type: ignore
    pass 
class Position:     # type: ignore
    pass 

# Errors
class DatasetNotFound(Exception):
    pass
class AlreadyInPosition(Exception):
    pass
class NotInPosition(Exception):
    pass

##
#   Reader Function
##
def read_stock(stock_name: str,  _from: str = "", _to: str = "", _field: str = "") -> pd.DataFrame:
    """ Read csv stock. Reading logic goes here """

    try:
        df = pd.read_csv(DATA_PATH + stock_name + CSV_EXT)
    except FileNotFoundError as error: raise DatasetNotFound(f"Dataset not found, please download your stock data: {stock_name}")

    df.index = df.Date

    if not _from and not _to:
        return  pd.DataFrame(df)

    if not _to:
        return pd.DataFrame(df[(df.Date > _from)])

    return pd.DataFrame(df[(df.Date > _from) & (df.Date <= _to)])

##
#   Implements a stock function for each. We can make it dynamic later on.
#   If we bundle everything into a library, this code should not be part of it.
#   For now it kept here just to keep it organized.
##
def AAPL(_from: str = "", _to: str = "") -> pd.DataFrame:
    return read_stock("AAPL", _from, _to)

def IBM(_from: str = "", _to: str = "") -> pd.DataFrame:
    return read_stock("IBM", _from, _to)

def MSFT(_from: str = "", _to: str = "") -> pd.DataFrame:
    return read_stock("MSFT", _from, _to)

##
#   Classes for data management
##
    
# TODO : Broker Trade Class, Orders Class (those are just structures to hold needed stuff)
# Broker should encapsulate : Trade, Orders, Position ?
# Might be overkill because we would need to find a really generic solution between brokers.
# Duck typing might be the key here to avoid fake inheritance.
@dataclass
class Position:
    """ Position class. Keep track of symbol positions. """
    symbol: str = field(repr=True)
    #value: int = field(repr=True)
    quantity: int = field(repr=True)
    enter_price: float = field(repr=True)
    enter_date: str = field(repr=True)

    def get_quantity(self) -> int:
        """ Returns the quantity of the position """
        return self.quantity

    def get_symbol(self) -> str:
        """ Returns the symbol of the position. """
        return self.symbol
    
    @staticmethod
    def load_positions(file_path: str) -> list[Position]: # type: ignore
        """ Theortically, we can have ongoing orders before debuting a strategy (for example comming from another strategy). """
        pass

@dataclass
class Order:
    """ Order class. To keep track of any information relatively of an order. """
    
    @staticmethod
    def load_orders(file_path: str) -> list[Order]: # type: ignore
        """ Theortically, we can have ongoing orders before debuting a strategy (for example comming from another strategy). """
        pass

@dataclass
class Trade:
    """ Trade class. To keep track of closed orders. """
    pass

@dataclass
class _Array(np.ndarray):
    """ Array as numpy encapsulation for performances. """

@dataclass
class _Data:
    """ Data class to hold and interact with data efficiently. """

    _df: pd.DataFrame = field(repr=False)
    __i: int = field(init=False)
    __cache: Dict[str, _Array] = field(repr=False)
    __arrays: Dict[str, _Array] = field(repr=False)

    def __post_init__(self):
        self.__i = len(self._df)

    def __getitem__(self, item):
        return self.__get_array(item)

    def __get_array(self, key) -> _Array:
        arr = self.__cache.get(key)
        if arr is None:
            arr = self.__cache[key] = cast(_Array, self.__arrays[key][:self.__i])
        return arr

@dataclass
class Broker:
    """ A Broker class. Will enable duck typing for different APIs. """

    cash_amount: float = field(repr=True, default=1000)

    _: KW_ONLY
    position: Optional[Position] = field(repr=True, default=None)       # Default empty if no existing position pre deployment
    orders: list[Order] = field(repr=True, default_factory=list)        # Default empty if no existing orders pre deployment
    trades: list[Trade] = field(repr=True, default_factory=list)        # Always empty : don't track pre deployment trades (no sense)

    @property
    def in_position(self) -> bool:
        """ Boolean to use in strategies. """
        return True if (self.position) else False

    def compute_value(self, price: float) -> float :
        return price * self.position.get_quantity() if self.position else 0

    def get_position(self) -> Optional[Position]:
        return self.position if self.position else None
    
    def get_orders(self) -> list[Order]:
        return self.orders

    def create_position(self, symbol: str, price: float, date: str):
        """ Create a position. Should be the work of the Order (if successfull). """
        if self.position: raise AlreadyInPosition("Can't enter because already in position.")
        max_quantity = int(self.cash_amount // price)
        self.cash_amount -= price * max_quantity         # Update the cash available
        self.position =  Position(symbol, max_quantity, price, date)

    def close_position(self, price: float, date:str):
        """ Close a position. Should be the work of the Order (if successfull). """
        if not self.position: raise NotInPosition("Can't exit because not in position.")

        self.cash_amount += self.position.get_quantity() * price
        self.position = None

    def enter(self, symbol: str, price: float, date: str):

        self.create_position(symbol, price, date)
        print(f"\tEntering symbol {symbol}: ", self.position)

    def exit(self, symbol: str, price: float, date: str):

        self.trades.append(self.close_position(price, date))
        print(f"\tExiting symbol {symbol}: ", self.cash_amount, self.position)

    def exit_all(self, symbol: str, price: float, date: str):
        self.exit(symbol, price, date)


##
#   Utils function
##

def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func
    
def get_function_name(func: Callable) -> str:
    return func.__name__