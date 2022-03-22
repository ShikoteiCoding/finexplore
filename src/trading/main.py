from dotenv import load_dotenv
from pathlib import Path
import os
import yfinance
from functools import partial

from rule import *
from strategy import *

def main() -> None:
    # Running the env file
    load_dotenv(dotenv_path = 'setup.env')

    # Loading Env Variables (pure demo)
    ALPACA_USER = os.getenv('ALPACA_USER')
    ALPACA_PWD  = os.getenv('ALPACA_PWD')

    # Connection to broker
    broker = Broker()
    broker.connect()

    # Strategy values
    buy_strategy = partial(should_buy_avg, window_size=30)
    sell_strategy = partial(should_sell_avg, window_size=200)

    strategy = RuleBasedStrategy(broker, buy_strategy, sell_strategy)
    strategy.run("BTC/USD")

if __name__ == '__main__':
    main()