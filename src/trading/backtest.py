import pandas as pd
import numpy as np

from typing import Callable

DATA_PATH = "../../data/companies_stock/"
CSV_EXT = ".csv"

class BackTest:
    """ Backtest Data Generator. """

    def __init__(self, stock_name: str, strategy: Callable, _from: str = "", _to: str = "", _field: str = "Close"):
        """ Init the object. """
        self.strategy: Callable = strategy
        self.df: pd.DataFrame = self.read_stock_data(stock_name, _from, _to, _field)
        self.past_data: pd.DataFrame = pd.DataFrame()

    def read_stock_data(self, stock_name: str, _from: str = "", _to: str = "", _field: str = "") -> pd.DataFrame:
        """ Read a stock from string name. """
        df = pd.read_csv(DATA_PATH + stock_name + CSV_EXT)
        df.index = df.Date

        if not _from and not _to:
            return  pd.DataFrame(df[_field])

        if not _to:
            return pd.DataFrame(df[(df.Date > _from)][_field])

        return pd.DataFrame(df[(df.Date > _from) & (df.Date <= _to)][_field])
        

    def run(self):
        """ Run the script iteratively.  """

        ##
        #   Backtest Object keep the responsability over data !
        #   Why ? Because the strategy does not know if it is live or trained data
        #   In trained data: we have all the data available, so we can pass a dataframe
        #   In "live data": we only have the newest data, so we need to be passed the history in addition
        #   History need thus to be computed at the above encapsulation level
        #   Consequences : Indicators or whatever needs to be calculated in the Stragegy from passed historic data
        #
        #   Warning : for performance reasons, passing a too big dataframe might lead to over memory contraint
        #   and slow the computation of Indicators. We have to find a way for the "Data Manager" to know the max_size of history
        #   it needs to be provided to the strategy.
        ##
        for row in self.df.iterrows():
            self.past_data = pd.concat([self.past_data, pd.Series(row)], axis = 0, ignore_index=False)
            self.strategy(row, self.past_data)