from dataclasses import KW_ONLY, dataclass, field
import datetime

from strategy import Decision, StrategyCallable
from _utils import DatasetReaderCallable, get_function_name, Data, Array
from broker import Broker

import pandas as pd
import numpy as np

DATA_PATH = "../../data/companies_stock/"
CSV_EXT = ".csv"

@dataclass()
class BackTest:
    """ Backtest Data Generator. """

    _broker:     Broker                 = field(init=True, repr=True)
    _stock_data: DatasetReaderCallable  = field(init=True, repr=False)
    _strategy:   StrategyCallable       = field(init=True, repr=False)
    
    _: KW_ONLY
    _commission_rate: float = field(init=True, repr=True, default=0)

    _strategy_name: str = field(init=False, repr=True)
    _symbol:        str = field(init=False, repr=True)

    ##
    #   TODO: Where to define indicators to plot ?
    ##
    def __post_init__(self):
        self._data:          Data   = self._stock_data()
        self._symbol:        str    = get_function_name(self._stock_data)
        self._strategy_name: str    = get_function_name(self._strategy)

        self._data.add_empty_array("equity")

    @property
    def broker(self) -> Broker:
        return self._broker
    
    @property
    def data(self) -> Data:
        return self._data
    
    @property
    def symbol(self) -> str:
        return self._symbol

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

        # TODO: Start should skip (in the backtest) the first data where
        # The indicators are not ready (returning NaN anyway)
        # start = 0 + max(windiw_size over indicators)
        # Make sure to start at 1 because we always want to look at least previous data
        # If not clear enough, make it a warning ?
        start = 1

        for i in range(start, self._data.len + 1):
            self._data.i = i

            price, decision = self._strategy(self._data, self._broker)

            # TODO: Will need to convert the index to a datetime object later on.
            index = str(self._data.Date[-1])

            # TODO: Should a strategy return an order instead?
            # Not sure of the Decision ENUM return anyway
            if not price:
                continue
            elif decision == Decision.ENTER:
                self._broker.buy(self._symbol, self._broker.max_long(price), price, index)
            elif decision == Decision.EXIT:
                self._broker.sell(self._symbol, - self._broker.max_short(), price, index)
            
            self._broker.process_orders(self._symbol, price, index)
            print(self._broker._position)

        # From backtesting py
        #equity = pd.Series(broker._equity).bfill().fillna(broker._cash).values
        #   self._results = compute_stats(
        #       trades=broker.closed_trades,
        #       equity=equity,
        #       ohlc_data=self._data,
        #       risk_free_rate=0.0,
        #       strategy_instance=strategy,
        #   )