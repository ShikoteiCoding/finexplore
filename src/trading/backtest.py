from dataclasses import KW_ONLY, InitVar, dataclass, field
from enum import Enum
from attr import frozen
import pandas as pd
import numpy as np

from typing import Callable

DATA_PATH = "../../data/companies_stock/"
CSV_EXT = ".csv"

# Testing for now
@dataclass
class Position:
    
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

# Testing for now
class Decision(Enum):
    ENTER = 1
    HOLD = 0
    EXIT = -1

@dataclass(frozen=False)
class BackTest:
    """ Backtest Data Generator. """

    stock_name: str
    strategy: Callable = field(repr = False)
    
    _: KW_ONLY
    _from: InitVar[str] = ""
    _to: InitVar[str] = ""
    _field: str = "Close"

    _df: pd.DataFrame = field(repr=False, init=False)
    _position: Position = field(repr=True, default = Position())

    def __post_init__(self, _from: str, _to: str):
        self._df: pd.DataFrame = self.read_stock_data(self.stock_name, _from, _to, self._field)
        # For now let's stock the past data as a numpy array
        self.data: np.ndarray = np.empty(shape=1)

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