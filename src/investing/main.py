import yfinance as yf
import pprint

from utils import load_json
from scrap import scrap_ishares_holdings

## Intersting URLs to scrap

# Ticker change in names: https://www.nasdaq.com/market-activity/stocks/symbol-change-history
# PER of companies: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/pedata.html
# Financial statements: https://www.sec.gov/dera/data/financial-statement-data-sets.html

def main():
    pp = pprint.PrettyPrinter(indent=2)

    DATA_PATH = 'data'
    ETF_PATH  = DATA_PATH + '/ETFs.json'

    etf_configs = load_json(ETF_PATH)

    for etf in etf_configs["tickers"]:
        holdings_url = etf["holdings_url"]
        holdings = scrap_ishares_holdings(holdings_url)

if __name__ == '__main__':
    main()