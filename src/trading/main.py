import os
from dataclasses import field
from functools import partial
from tkinter import N
import numpy as np

import pandas as pd
import talib as ta 
from dotenv import load_dotenv

from backtest import BackTest, Position, Decision
from broker import AlpacaBroker, DemoBroker, YFinance
from rule import *
from strategy import *


def example() -> None:

    # Connection to broker
    demo_broker = DemoBroker()
    demo_broker.connect()

    # Strategy values
    buy_strategy = partial(should_buy_avg, window_size=30)
    sell_strategy = partial(should_sell_minmax, min_price=38_000)

    strategy = DemoRuleBasedStrategy(
        broker = demo_broker,
        automate = demo_broker,
        marketdata = demo_broker,
        buy_strategy = buy_strategy,
        sell_strategy = sell_strategy)
    strategy.run("BTC/USD")

def alpaca_test() -> None:
    # Running the env file. Can become docker environment variable (env file ref) later on.
    load_dotenv(dotenv_path = "alpaca-paper.env")

    key_id = str(os.getenv("APCA_API_KEY_ID"))
    secret_key = str(os.getenv("APCA_API_SECRET_KEY"))
    base_url = str(os.getenv("APCA_API_BASE_URL"))

    alpaca_broker = AlpacaBroker(
        key_id = key_id,
        secret_key = secret_key,
        base_url = base_url
    )
    alpaca_broker.connect()
    alpaca_broker.check_connection()

def test_rule() -> None:
    """ Testing rule on historic data. """
    yfinance = YFinance()

    # Connection to broker
    broker = DemoBroker()
    broker.connect()

    # Strategy values
    buy_strategy = partial(should_buy_avg, window_size=30)
    sell_strategy = partial(should_sell_minmax, min_price=38_000)

    strategy = DemoRuleBasedStrategy(broker, broker, broker, buy_strategy, sell_strategy)
    strategy.run("BTC/USD")

    print(yfinance)

def backtest():
    # To move away
    def crossover(v1: int, v2: int) -> bool:
        """ Simple crossover function to keep code cleaner. """
        return v1 > v2

    # Shitty simple version : do we really need to know the position here ? A signal is a signal
    # Position logic can be deported in the runnable class TODO: Decide on that
    def sma(data: np.ndarray, position: Position) -> Decision:
        """ Simple Mobile Average Strategy """
        # This should work even if Runnable is not a backtest function but a websocket (for example ?) runnable (i.e: bot)
        
        ma1 = ta.SMA(data, 10)[-1]  # type: ignore
        ma2 = ta.SMA(data, 20)[-1]  # type: ignore

        if not position.holding and crossover(ma1, ma2):
            return Decision.ENTER
        elif position.holding and crossover(ma2, ma1):
            return Decision.EXIT
        return Decision.HOLD

    test = BackTest('AAPL', sma, _from = '2020-01-01', _to = '2021-01-01')

    test.run()

if __name__ == '__main__':
    backtest()