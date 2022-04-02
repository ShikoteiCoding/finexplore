from dotenv import load_dotenv
import os
from functools import partial

from rule import *
from strategy import *

from broker import AlpacaBroker, DemoBroker, YFinance

from backtest import BackTest

import pandas as pd

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

    # Shitty simple version
    def sma(data: pd.DataFrame, past_data: pd.DataFrame):
        pass


    test = BackTest('AAPL', sma, '2020-01-01', '2021-01-01')

    test.run()

if __name__ == '__main__':
    backtest()