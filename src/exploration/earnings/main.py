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

    #res = utils.load_sp_500_constituents(reload=False)
    #top_5_symbols = [row.symbol for _, row in res[:5].iterrows()]
    #earnings = utils.load_ticker_earnings_history(top_5_symbols, reload=False)
    #
    #print(utils.enrich_tickers_earnings_history(earnings))
    try:
        connection = psycopg2.connect(
            database=config.db_name,
            user=config.db_username,
            password=config.db_password,
            host=config.db_host,
            port=config.db_port
        )
    except Exception as e:
        raise Exception("Error: Please verify the connection provided")

    cursor = connection.cursor("test_query")
    query = "SELECT * FROM monthly_share_prices"
    cursor.execute(query=query)

    data = cursor.fetchall()
    cursor.close()

    print(pd.DataFrame(data))