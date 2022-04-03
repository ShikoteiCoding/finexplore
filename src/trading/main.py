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

def backtest1():
    # To move away
    

    # Shitty simple version : do we really need to know the position here ? A signal is a signal
    # Position logic can be deported in the runnable class TODO: Decide on that

    sma_partial = partial(sma, sma1_window_size=10, sma2_window_size=20)

    test = BackTest('MSFT', sma_partial, _from = '2019-01-01', _to = '2022-01-01')

    test.run()

if __name__ == '__main__':
    backtest1()