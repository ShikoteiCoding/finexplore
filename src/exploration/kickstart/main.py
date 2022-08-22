from tracemalloc import reset_peak
import utils
import pandas as pd
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import utils

if __name__ == "__main__":
    
    #mmm = yf.Ticker("MMM")
    #
    #data = mmm.history(start="2022-07-28", end="2022-07-29", interval="1m")
    res = utils.load_sp_500_constituents(reload=False)
    top_5_symbols = [row.symbol for _, row in res[:5].iterrows()]
    quaterly_releases = utils.load_ticker_earnings_history(top_5_symbols, reload=False)
    print(quaterly_releases)