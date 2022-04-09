from dataclasses import dataclass, field
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
#   Reader 
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
#   Implements a stock function for each. We can make it dynamic later on
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
class _Position:
    
    holding: bool = field(default=False)
    amount: float = field(default=1000)
    position: float = field(default=0)
    quantity_position: int = field(default=0) # If fraction are available, might need to change that

    def exit(self, price: float):
        prev_quantity = self.quantity_position
        self.amount, self.position, self.quantity_position = self.compute_exit(price)
        print(
            f"""
            Exiting position of {prev_quantity} positions at {price} each.
            Portfolio value is now {self.position} dollars.
            Buy power is now {self.amount} dollars.
            """)
        self.holding = False

    def enter(self, price: float):
        self.amount, self.position, self.quantity_position = self.compute_enter(price)
        print(
            f"""
            Entering position with {self.quantity_position} positions at {price} each.
            Portfolio value is now {self.position} dollars.
            Buy power is now {self.amount} dollars.
            """)
        self.holding = True

    def compute_enter(self, price: float) -> tuple[float, float, int]:
        """ Return the number of action to buy with available amount. """
        max_quantity = int(self.amount // price)
        left_amount = self.amount % price
        max_position = price * max_quantity
        return (left_amount, max_position, max_quantity)

    def compute_exit(self, price: float) -> tuple[float, float, int]:
        """ Return the number of action to buy with available amount. """
        max_quantity = 0
        left_amount = self.amount + self.quantity_position * price
        max_position = 0
        return (left_amount, max_position, max_quantity)

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