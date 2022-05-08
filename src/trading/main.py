import os
from dotenv import load_dotenv

from backtest import BackTest
from broker import AlpacaBroker
from strategy import simple_mobile_average, simple_bollinger_bands

from _utils import MSFT, AAPL, IBM, wrapped_partial, get_function_name, Data
from broker import Broker
from plotting import backtest_dashboard, _temporal_reduce, Temporality
import dash


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
    broker = Broker(_cash_amount=1_000_000)
    stock_data = wrapped_partial(AAPL, _from = "2021-01-01")
    sma_partial = wrapped_partial(simple_mobile_average, sma1_window_size=10, sma2_window_size=20)

    test = BackTest(broker, stock_data, sma_partial)

    test.run()

def backtest_bbands():
    """ Testing new data import """
    broker = Broker(_cash_amount=1_000)
    stock_data = wrapped_partial(AAPL, _from = "2021-01-01")
    sbband_partial = wrapped_partial(simple_bollinger_bands, sma1_window_size=14, bband_window_size=21)

    test = BackTest(broker, stock_data, sbband_partial, _commission_rate=0.02)

    test.run()

    print(test.data.equity)

def plot():
    """ Testing the Plotting. """
    broker = Broker(_cash_amount=1_000, _debug=False)
    stock_data = wrapped_partial(AAPL, _from = "2021-01-01")
    sbband_partial = wrapped_partial(simple_bollinger_bands, sma1_window_size=14, bband_window_size=21)

    test = BackTest(broker, stock_data, sbband_partial, _commission_rate=0.001)
    test.run()

    data = test.data

    app = dash.Dash()

    app = backtest_dashboard(app, get_function_name(AAPL), data)
    
    app.run_server(debug=True)
    
if __name__ == '__main__':
    plot()