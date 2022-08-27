import utils
import pandas as pd
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import utils
import psycopg2
import dotenv
from psycopg2 import sql

from config import Config, load_config as load, load_db_opts, load_polygon_opts

if __name__ == "__main__":
    # Load local dotenv (because not dockerize for now - can be added to image or passed at docker run)
    dotenv.load_dotenv(utils.ENV_DOCKER_FILE)
    dotenv.load_dotenv(utils.ENV_SECRETS_FILE)
    config = load(load_db_opts, load_polygon_opts)

    #connection = utils.psql_connect(config)

    tickers = ["MMM"]
    #print(utils._scrap_opening_minutes_earning_date(tickers[0], datetime.datetime(2022, 7, 26), datetime.datetime(2022, 7, 26)))
    print(config)

    #connection.close()