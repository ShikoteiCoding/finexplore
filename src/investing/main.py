import yfinance as yf

from utils import load_json

## Intersting URLs to scrap

# Ticker change in names: https://www.nasdaq.com/market-activity/stocks/symbol-change-history
# PER of companies: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/pedata.html
# Financial statements: https://www.sec.gov/dera/data/financial-statement-data-sets.html

def main():

    DATA_PATH = 'data'
    ETF_PATH  = DATA_PATH + '/ETFs.json'

    etf_configs = load_json(ETF_PATH)
    print(etf_configs)



if __name__ == '__main__':
    main()