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
DatasetReader = Callable[[],pd.DataFrame]

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