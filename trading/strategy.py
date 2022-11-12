from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, TypeAlias, Optional

from utils import Data
from broker import Broker

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

    def __int__(self):
        return self.value

## 
#   Strategy Callable
##
StrategyCallable: TypeAlias = Callable[[Data, Broker], tuple[Optional[float], Decision]]

# broker logic can be deported in the runnable class TODO: Decide on that
# broker should be a list of broker instead ?
def simple_mobile_average(data: Data, broker: Broker, sma1_window_size=20, sma2_window_size=50) -> tuple[float, Decision]:
        """ Simple Mobile Average Strategy """
        prices = data.Close
        
        ma1 = ta.SMA(prices, sma1_window_size)[-1]  # type: ignore
        ma2 = ta.SMA(prices, sma2_window_size)[-1]  # type: ignore

        if not broker.in_position and crossover(ma1, ma2):
            return prices[-1], Decision.ENTER
        elif broker.in_position and crossover(ma2, ma1):
            return prices[-1], Decision.EXIT
        return prices[-1], Decision.HOLD

def simple_bollinger_bands(data: Data, broker: Broker, sma1_window_size=14, bband_window_size=21) -> tuple[float, Decision]:
        """ Simple BBand Strategy """
        prices = data.Close
        
        ma1 = ta.SMA(prices, sma1_window_size)[-1]  # type: ignore
        _, _, lowerband = ta.BBANDS(prices, bband_window_size)  # type: ignore

        last_price = prices[-1]
        last_bband = lowerband[-1]

        if not broker.in_position and crossover(last_price, last_bband):
            return prices[-1], Decision.ENTER
        elif broker.in_position and crossover(ma1, last_price):
            return prices[-1], Decision.EXIT
        return prices[-1], Decision.HOLD