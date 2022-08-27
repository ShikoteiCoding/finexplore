import utils
import pandas as pd
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import utils
import psycopg2
import dotenv
from psycopg2 import sql

from config import Config, load_config as load, load_db_opts

if __name__ == "__main__":
    # Load local dotenv (because not dockerize for now - can be added to image or passed at docker run)
    dotenv.load_dotenv(utils.ENV_FILE)
    config = load(load_db_opts)

    connection = utils.psql_connect(config)

    tickers = ["MMM"]

    data = utils.first_protocol(tickers, connection)
    print(data)
    #utils.ingest_tickers_earnings_history_and_daily_share_prices(connection, tickers, reload=True)

    #print(utils.psql_fetch(sql.SQL(
    #    """
    #    SELECT
    #        T.earnings_date,
    #        to_char(earnings_date, 'Day')   AS earnings_weekday,
    #        T.symbol,
    #        P.open,
    #        P.high,
    #        P.low,
    #        P.close
    #    FROM tickers_earnings_history AS T
    #    LEFT JOIN tickers_daily_share_prices AS P
    #        ON T.symbol = P.symbol AND DATE_TRUNC('day', T.earnings_date) = DATE_TRUNC('day', P.date)
    #    WHERE TRUE
    #        AND T.symbol in ({tickers})
    #        AND T.eps_reported IS NOT NULL
    #    --ORDER BY T.earnings_date DESC
    #    """
    #).format(tickers=sql.SQL(',').join([sql.Literal(ticker) for ticker in tickers])), connection))

    connection.close()