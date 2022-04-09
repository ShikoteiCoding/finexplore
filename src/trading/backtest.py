from dataclasses import KW_ONLY, dataclass, field
import datetime

from strategy import Decision, StrategyCallable
from _utils import Position, _Data, DatasetReaderCallable, Broker, get_function_name

import pandas as pd
import numpy as np

DATA_PATH = "../../data/companies_stock/"
CSV_EXT = ".csv"

@dataclass(frozen=False)
class BackTest:
    """ Backtest Data Generator. """

    broker: Broker
    stock_data: DatasetReaderCallable
    strategy: StrategyCallable = field(repr=False)
    
    _: KW_ONLY
    _field: str = "Close"

    _df: pd.DataFrame = field(repr=False, init=False)
    _symbol: str = field(repr=True, init=False)
    #Position: Position = field(repr=True, default=Position()) # Might not be accurate. To think upon.

    ##
    #   Where to define indicators to plot ?
    ##

    def __post_init__(self):
        self._df: pd.DataFrame = pd.DataFrame(self.stock_data()[self._field])
        # For now let's stock the past data as a numpy array
        self.data: np.ndarray = np.empty(shape=1)
        self._symbol: str = get_function_name(self.stock_data)
    

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
            decision = self.strategy(self.data, self.broker)

            # Will need to convert the index to a datetime object later on.

            if decision == Decision.ENTER:
                print(f"\nDate is: {index}")
                self.broker.enter(self._symbol, current_price, str(index))
            if decision == Decision.EXIT:
                print(f"\nDate is: {index}")
                self.broker.exit(self._symbol, current_price, str(index))
        
        # Exit no matter what do evaluate performances
        self.broker.exit_all(self._symbol, self._df.Close[-1], str(self._df.index[-1]))