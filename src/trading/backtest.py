from dataclasses import KW_ONLY, InitVar, dataclass, field
from enum import Enum
import pandas as pd
import numpy as np

from typing import Callable

DATA_PATH = "../../data/companies_stock/"
CSV_EXT = ".csv"

# Testing for now
@dataclass
class Position:
    
    holding: bool = field(default = False)
    amount: int = field(default=0)

    def exit(self):
        self.holding = False

    def enter(self):
        self.holding = True

# Testing for now
class Decision(Enum):
    ENTER = 1
    HOLD = 0
    EXIT = -1

@dataclass
class BackTest:
    """ Backtest Data Generator. """

    stock_name: str
    strategy: Callable = field(repr = False)
    
    _: KW_ONLY
    _from: InitVar[str] = ""
    _to: InitVar[str] = ""
    _field: InitVar[str] = "Close"

    _df: pd.DataFrame = field(repr=False, init=False)
    _position: Position = field(repr=True, default = Position())

    def __post_init__(self, _from: str, _to: str, _field: str):
        self._df: pd.DataFrame = self.read_stock_data(self.stock_name, _from, _to, _field)
        # For now let's stock the past data as a numpy array
        self.past_data: np.ndarray = np.empty(shape=1)

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
        #
        #   Advantages : Data can be accessed from a class and strategy can stay a function (TODO: define the callable signature)
        ##
        for index, row in self._df.iterrows():
            # Past data is appended with current data and provided to the strategy to make decision
            self.past_data = np.append(self.past_data, row.Close)  
            self.strategy(self.past_data, self._position)