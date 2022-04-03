import os
from dataclasses import field
from functools import partial
from tkinter import N
import numpy as np

import pandas as pd
import talib as ta 
from dotenv import load_dotenv

from backtest import BackTest, Position, Decision
from broker import AlpacaBroker, YFinance
from rule import *
from strategy import *

from stock_data import MSFT, AAPL, IBM


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

def test():
    """ Testing new data import """
    stock_data = partial(AAPL, _from = "2021-01-01")
    sma_partial = partial(sma, sma1_window_size=10, sma2_window_size=20)

    test = BackTest(stock_data, sma_partial)

    test.run()

if __name__ == '__main__':
    test()