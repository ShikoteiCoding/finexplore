from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, TypeAlias

from _utils import Data, Broker, Array

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
#   Strategy Callable
##
StrategyCallable: TypeAlias = Callable[[Array, Broker], Decision]

# broker logic can be deported in the runnable class TODO: Decide on that
# broker should be a list of broker instead ?
def simple_mobile_average(data: np.ndarray, broker: Broker, sma1_window_size=20, sma2_window_size=50) -> Decision:
        """ Simple Mobile Average Strategy """
        # This should work even if Runnable is not a backtest function but a websocket (for example ?) runnable (i.e: bot)
        
        ma1 = ta.SMA(data, sma1_window_size)[-1]  # type: ignore
        ma2 = ta.SMA(data, sma2_window_size)[-1]  # type: ignore

        if not broker.in_position and crossover(ma1, ma2):
            return Decision.ENTER
        elif broker.in_position and crossover(ma2, ma1):
            return Decision.EXIT
        return Decision.HOLD

def simple_bollinger_bands(data: Array, broker: Broker, sma1_window_size=14, bband_window_size=21) -> Decision:
        """ Simple BBand Strategy """
        
        # This should work even if Runnable is not a backtest function but a websocket (for example ?) runnable (i.e: bot)
        ma1 = ta.SMA(data, sma1_window_size)[-1]  # type: ignore
        _, _, lowerband = ta.BBANDS(data, bband_window_size)  # type: ignore

        last_price = data[-1]

        last_bband = lowerband[-1]

        if not broker.in_position and crossover(last_price, last_bband):
            return Decision.ENTER
        elif broker.in_position and crossover(ma1, last_price):
            return Decision.EXIT
        return Decision.HOLD