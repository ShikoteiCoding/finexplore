import os
from functools import partial
from re import M
from dotenv import load_dotenv

from backtest import BackTest
from broker import AlpacaBroker
from strategy import simple_mobile_average, simple_bollinger_bands

from _utils import MSFT, AAPL, IBM, Broker, wrapped_partial, _Data


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

def backtest_ma():
    """ Testing new data import """
    broker = Broker(cash_amount=1_000_000)
    stock_data = wrapped_partial(AAPL, _from = "2021-01-01")
    sma_partial = wrapped_partial(simple_mobile_average, sma1_window_size=10, sma2_window_size=20)

    test = BackTest(broker, stock_data, sma_partial)

    test.run()

def backtest_bbands():
    """ Testing new data import """
    broker = Broker(cash_amount=1_000)
    stock_data = wrapped_partial(AAPL, _from = "2021-01-01")
    sbband_partial = wrapped_partial(simple_bollinger_bands, sma1_window_size=14, bband_window_size=21)

    test = BackTest(broker, stock_data, sbband_partial)

    test.run()

def test_data():
    """ Testing the new data class. """

    data = AAPL()
    print(data)
    print(data.Close)


    
if __name__ == '__main__':
    backtest_bbands()