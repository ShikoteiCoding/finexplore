from dataclasses import KW_ONLY, InitVar, dataclass, field
from strategy import _Position, Decision, sma, Strategy
import pandas as pd
import numpy as np

from typing import Callable
from stock_data import DatasetReader

DATA_PATH = "../../data/companies_stock/"
CSV_EXT = ".csv"

@dataclass(frozen=False)
class BackTest:
    """ Backtest Data Generator. """

    stock_data: DatasetReader
    strategy: Strategy = field(repr = False)
    
    _: KW_ONLY
    _field: str = "Close"

    _df: pd.DataFrame = field(repr=False, init=False)
    _position: _Position = field(repr=True, default = _Position()) # Might not be accurate. To think upon.

    ##
    #   Where to define indicators to plot ?
    ##

    def __post_init__(self):
        self._df: pd.DataFrame = pd.DataFrame(self.stock_data()[self._field])
        # For now let's stock the past data as a numpy array
        self.data: np.ndarray = np.empty(shape=1)
    

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
            current_price: float = row[self._field]  # type: ignore
            # Past data is appended with current data and provided to the strategy to make decision
            self.data = np.append(self.data, current_price) # type: ignore
            decision = self.strategy(self.data, self._position)

            if decision == Decision.ENTER:
                print(f"\nDate is: {index}")
                self._position.enter(current_price)
            if decision == Decision.EXIT:
                print(f"\nDate is: {index}")
                self._position.exit(current_price)