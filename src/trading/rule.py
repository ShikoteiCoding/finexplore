##
#   Layout of Functionnal Strategy Pattern
##
import statistics
from typing import Callable

# Rule Function Signature
TradingStrategyRule = Callable[[list[int]], bool]

def should_buy_avg(prices: list[int], window_size: int) -> bool:
    # Make a decision based on 
    list_window = prices[-window_size:]
    return prices[-1] < statistics.mean(list_window)


def should_sell_avg(prices: list[int], window_size: int) -> bool:
    list_window = prices[-window_size:]
    return prices[-1] > statistics.mean(list_window)


def should_buy_minmax(prices: list[int], max_price: int) -> bool:
    # buy if it's below the max price
    return prices[-1] < max_price


def should_sell_minmax(prices: list[int], min_price: int) -> bool:
    # sell if it's above the min price
    return prices[-1] > min_price