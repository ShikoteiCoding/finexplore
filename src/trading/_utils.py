from dataclasses import KW_ONLY, dataclass, field
from typing import Dict, cast
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
#   Signatures
##
DatasetReaderCallable = Callable[[],pd.DataFrame]

##
#   Errors 
##
class DatasetNotFound(Exception):
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
#   Classes for data organisation
##

    
# TODO : Broker Trade Class, Orders Class (those are just structures to hold needed stuff)
# Broker should encapsulate : Trade, Orders, Position ?
# Might be overkill because we would need to find a really generic solution between brokers.
# Duck typing might be the key here to avoid fake inheritance.
@dataclass
class Position:
    """ Position class. Keep track of symbol positions. """
    symbol: str = field(repr=True)
    value: int = field(repr=True)

@dataclass
class Order:
    """ Order class. To keep track of any information relatively of an order. """
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

    cash_amount: int = field(repr=True, default=1000)

    _: KW_ONLY
    positions: list[Position] = field(repr=True, default_factory=list)
    orders: list[Order] = field(repr=True, default_factory=list)
    trades: list[Trade] = field(repr=True, default_factory=list)
    
    holding: bool = field(default=False)
    amount: float = field(default=1000)
    position: float = field(default=0)
    quantityPosition: int = field(default=0) # If fraction are available, might need to change that

    @property
    def in_position(self):
        """ Boolean to use in strategies. """
        return len(self.positions) > 0

    def get_positions(self):
        return self.positions
    
    def get_orders(self):
        return self.orders

    def exit(self, price: float):
        prev_quantity = self.quantityPosition
        self.amount, self.position, self.quantityPosition = self.compute_exit(price)
        print(
            f"""
            Exiting position of {prev_quantity} positions at {price} each.
            Portfolio value is now {self.position} dollars.
            Buy power is now {self.amount} dollars.
            """)
        self.holding = False

    def enter(self, price: float):
        self.amount, self.position, self.quantityPosition = self.compute_enter(price)
        print(
            f"""
            Entering position with {self.quantityPosition} positions at {price} each.
            Portfolio value is now {self.position} dollars.
            Buy power is now {self.amount} dollars.
            """)
        self.holding = True

    def compute_enter(self, price: float) -> tuple[float, float, int]:
        """ Return the number of action to buy with available amount. """
        max_quantity = int(self.amount // price)
        left_amount = self.amount % price
        maxPosition = price * max_quantity
        return (left_amount, maxPosition, max_quantity)

    def compute_exit(self, price: float) -> tuple[float, float, int]:
        """ Return the number of action to buy with available amount. """
        max_quantity = 0
        left_amount = self.amount + self.quantityPosition * price
        maxPosition = 0
        return (left_amount, maxPosition, max_quantity)