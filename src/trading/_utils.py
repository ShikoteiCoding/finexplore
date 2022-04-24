from dataclasses import dataclass, field
from functools import partial, update_wrapper
from typing import Callable, Dict, TypeAlias, cast

import numpy as np
import pandas as pd

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
    
    def to_series(self) -> pd.Series:
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

    @property
    def df(self) -> pd.DataFrame:
        original_columns = self._df.columns
        for column in self.columns:
            if column not in original_columns:
                arr = self.__arrays[column]
                self._df[column] = arr.to_series()
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
        self.__arrays[__name] = Array(np.tile(np.nan, self.__len), name=__name, index=self._df.index.copy())

    def to_pandas(self) -> pd.DataFrame:
        return self._df


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
