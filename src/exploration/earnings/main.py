import utils
import pandas as pd
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import utils
import psycopg2
import dotenv

from config import Config, load_config as load, load_db_opts

if __name__ == "__main__":
    # Load local dotenv (because not dockerize for now - can be added to image or passed at docker run)
    dotenv.load_dotenv(utils.ENV_FILE)
    config = load(load_db_opts)

    connection = utils.psql_connect(config)

    tickers = ["MMM"]

    #data = utils.first_protocol(tickers, connection)
    #print(data)
    utils.ingest_tickers_earnings_history_and_daily_share_prices(connection, tickers, reload=True)

    connection.close()