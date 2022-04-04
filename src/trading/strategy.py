from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

import numpy as np
import talib as ta


##
#   Strategy Utils
##
def crossover(v1: int, v2: int) -> bool:
        """ Simple crossover function to keep code cleaner. """
        return v1 > v2

class Decision(Enum):
    ENTER = 1
    HOLD = 0
    EXIT = -1

##
#   Utilities
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

## 
#   Strategy Callable
##
Strategy = Callable[[np.ndarray, _Position], Decision]

# Position logic can be deported in the runnable class TODO: Decide on that
# Position should be a list of position instead ?
def sma(data: np.ndarray, position: _Position, sma1_window_size=20, sma2_window_size=50) -> Decision:
        """ Simple Mobile Average Strategy """
        # This should work even if Runnable is not a backtest function but a websocket (for example ?) runnable (i.e: bot)
        
        ma1 = ta.SMA(data, sma1_window_size)[-1]  # type: ignore
        ma2 = ta.SMA(data, sma2_window_size)[-1]  # type: ignore

        if not position.holding and crossover(ma1, ma2):
            return Decision.ENTER
        elif position.holding and crossover(ma2, ma1):
            return Decision.EXIT
        return Decision.HOLD