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
    #    WITH daily_prices AS (
    #        SELECT
    #            symbol,
    #            date,
    #            open,
    #            close,
    #            high,
    #            low,
    #            LAG(date, 1) OVER (PARTITION BY symbol ORDER BY date DESC) AS next_date
    #        FROM tickers_daily_share_prices
    #    )
    #    SELECT
    #        T.earnings_date,
    #        to_char(earnings_date, 'Day')   AS earnings_weekday,
    #        T.symbol,
    #        P.open  AS open_current_day,
    #        P.high  AS high_current_day,
    #        P.low   AS low_current_day,
    #        P.close AS close_current_day,
    #        P1.open  AS open_previous_day,
    #        P1.high  AS high_previous_day,
    #        P1.low   AS low_previous_day,
    #        P1.close AS close_previous_day 
    #    FROM tickers_earnings_history AS T
    #    LEFT JOIN daily_prices AS P
    #        ON T.symbol = P.symbol AND DATE_TRUNC('day', T.earnings_date) = DATE_TRUNC('day', P.date)
    #    LEFT JOIN daily_prices AS P1
    #        ON T.symbol = P1.symbol AND DATE_TRUNC('day', T.earnings_date) = DATE_TRUNC('day', P1.next_date)
    #    WHERE TRUE
    #        AND T.symbol in ({tickers})
    #        AND T.eps_reported IS NOT NULL
    #    ORDER BY T.earnings_date DESC
    #    """
    #).format(tickers=sql.SQL(',').join([sql.Literal(ticker) for ticker in tickers])), connection))

    connection.close()