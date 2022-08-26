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

    #utils.ingest_tickers_monthly_prices(connection, tickers, start_date=datetime.datetime(1998, 1, 1), end_date=datetime.datetime.now())
    #utils.ingest_tickers_earnings_history(connection, tickers, reload=True)

    utils.ingest_sp_500_constituents(connection)

    connection.close()