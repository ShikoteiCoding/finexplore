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

if __name__ == '__main__':
    alpaca_test()