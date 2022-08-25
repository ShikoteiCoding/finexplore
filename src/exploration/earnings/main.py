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

    #utils.load_monthly_prices(connection, ["MMM"], start_date=datetime.datetime(1998, 1, 1), end_date=datetime.datetime.now())

    df = utils.psql_get_result("SELECT * FROM monthly_share_prices", connection)
    print(df)

    connection.close()