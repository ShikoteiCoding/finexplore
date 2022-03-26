from dotenv import load_dotenv
from pathlib import Path
import os
from functools import partial

from rule import *
from strategy import *

from broker import AlpacaBroker

def example() -> None:

    # Connection to broker
    broker = Broker()
    broker.connect()

    # Strategy values
    buy_strategy = partial(should_buy_avg, window_size=30)
    sell_strategy = partial(should_sell_avg, window_size=200)

    strategy = RuleBasedStrategy(broker, buy_strategy, sell_strategy)
    strategy.run("BTC/USD")

def alpaca_test() -> None:
    # Running the env file
    load_dotenv(dotenv_path = 'setup.env')

    # Loading Env Variables (pure demo)
    ALPACA_PAPER_KEY_ID = os.getenv('ALPACA_PAPER_KEY_ID')
    ALPACA_PAPER_SECRET_KEY  = os.getenv('ALPACA_PAPER_SECRET_KEY')

    alpaca_broker = AlpacaBroker(ALPACA_PAPER_KEY_ID, ALPACA_PAPER_SECRET_KEY)
    alpaca_broker.connect()

if __name__ == '__main__':
    alpaca_test()