from tracemalloc import reset_peak
import utils
import pandas as pd
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import utils

if __name__ == "__main__":

    res = utils.load_sp_500_constituents(reload=False)
    top_5_symbols = [row.symbol for _, row in res[:5].iterrows()]
    earnings = utils.load_ticker_earnings_history(top_5_symbols, reload=False)

    filtered_earnings = earnings[earnings["eps_reported"].notnull()]

    last_15_releases = filtered_earnings.sort_values(by=["symbol", "earnings_date"], ascending=False).groupby("symbol").head(15)
    last_15_releases["day_following_report"] = last_15_releases["earnings_date"].apply(
        lambda x: 
        x
        if (
            datetime.time(x.hour) >= utils.str_to_hour(utils.OPENING_HOURS["EST"]["start"])
            and datetime.time(x.hour) < utils.str_to_hour(utils.OPENING_HOURS["EST"]["end"])
        )
        else x + datetime.timedelta(days=1)
    )
    print(last_15_releases)