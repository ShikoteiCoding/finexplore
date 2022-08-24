import utils
import pandas as pd
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import utils
import psycopg2

from config import Config, load_config as load, load_db_opts

if __name__ == "__main__":

    #res = utils.load_sp_500_constituents(reload=False)
    #top_5_symbols = [row.symbol for _, row in res[:5].iterrows()]
    #earnings = utils.load_ticker_earnings_history(top_5_symbols, reload=False)
    #
    #print(utils.enrich_tickers_earnings_history(earnings))

    config = load(load_db_opts)


    print(config)