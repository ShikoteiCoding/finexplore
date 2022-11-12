import yfinance as yf
import pprint
import pandas as pd
import json

from utils import load_json
from scrap import (
    scrap_ishares_holdings_download_link,
    download_ishares_holdings_data,
    convert_ishares_json_to_csv
)

## Intersting URLs to scrap

# Ticker change in names: https://www.nasdaq.com/market-activity/stocks/symbol-change-history
# PER of companies: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/pedata.html
# Financial statements: https://www.sec.gov/dera/data/financial-statement-data-sets.html

def main():
    pp = pprint.PrettyPrinter(indent=2)

    DATA_PATH = 'data'
    ETF_PATH  = DATA_PATH + '/ETFs.json'
    ISHARES_PATH = DATA_PATH + '/iShares'
    

    etf_configs = load_json(ETF_PATH)

    for etf in etf_configs["tickers"]:
        holdings_url = etf["holdings_url"]
        ticker = etf["ticker"]
        holdings_data_url = scrap_ishares_holdings_download_link(holdings_url)
        download_ishares_holdings_data(holdings_data_url[0], ticker + ".csv", ISHARES_PATH)

def test():
    data = pd.read_csv("data/iShares/ICLN.csv", skiprows=9)
    print(data.iloc[:-2 , :])

if __name__ == '__main__':
    test()