from config import Config
from yfinance import Ticker
from datapackage import Package

import pandas as pd
import numpy as np
import datetime
import requests

#--------------------------

USER_AGENT_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
METADATA = {
    "s&p500": {
        "columns": ["symbol","company","sector"],
        "index_label": "index"
    },
    "earnings_history": {
        "columns": ["symbol", "company", "earnings_date", "eps_estimates", "eps_reported", "surprise_percent"],
        "index_label": "index"
    },
    "monthly_prices": {
        "columns": ["open", "high", "low", "close", "volume", "dividends", "stock_splits", "symbol"],
        "index_label": "date"
    },
    "daily_prices": {
        "columns": ["open", "high", "low", "close", "volume", "dividends", "stock_splits", "symbol"],
        "index_label": "date"
    },
    "minute_prices": {
        "columns": ["open", "high", "low", "close", "volume", "dividends", "stock_splits", "symbol"],
        "index_label": "date"
    },
}

#--------------------------
def _scrap_sp_500_constituents(*, metadata:dict = METADATA["s&p500"]) -> pd.DataFrame:
    """ Scrap the S&P 500 constituents. """

    package = Package("https://datahub.io/core/s-and-p-500-companies/datapackage.json")
    resource = package.get_resource("constituents_csv")

    if not resource:
        print("[INFO]: Resource is empty. Consider fixing the get_sp_500_constituents() scrapping function.")
        return pd.DataFrame()

    return pd.DataFrame(resource.read(), columns=metadata["columns"])

def _scrap_previous_earnings(symbol:str, *, metadata:dict = METADATA["earnings_history"]) -> pd.DataFrame:
    """ Scrap the earnings report data from yfinance. """

    # TODO: Improve the scrapping by loading the other pages (data are paginated)
    url = f"https://finance.yahoo.com/calendar/earnings?symbol={symbol}"
    data = requests.get(url, headers=USER_AGENT_HEADER).text
    df = pd.DataFrame(columns=metadata["columns"])

    try:
        df = pd.read_html(data)[0]
        df.replace("-", np.nan, inplace=True)

        df['EPS Estimate'] = pd.to_numeric(df['EPS Estimate'])
        df['Reported EPS'] = pd.to_numeric(df['Reported EPS'])
        df['Earnings Date'] = pd.to_datetime(
            df['Earnings Date'].apply(lambda x: x[:-3]),  # Remove the timezone for now
            format="%b %d, %Y, %I %p"
        )
        df.columns = metadata["columns"]
    except ValueError:
        print(f"[INFO]: No available earnings data for {symbol}")

    return df

def _scrap_daily_prices_for_earnings(symbol:str, start_day:datetime.datetime, end_day:datetime.datetime, *, metadata:dict = METADATA["monthly_prices"]) -> pd.DataFrame:
    """ Scrap the daily prices. Using yfinance library. """
    ticker = Ticker(symbol)

    df:pd.DataFrame = ticker.history(start=start_day, end=end_day, interval="1d", auto_adjust=False, back_adjust=False)

    df = df.drop('Adj Close', axis=1)

    # Renaming as the scrapping is not self made
    df = df.rename(columns=dict(zip(list(df.columns), metadata["columns"][:-1])))
    df.index.name = metadata["index_label"]

    df = df[df["open"].notnull()]
    df["symbol"] = symbol
    df = df.reset_index()

    return df

def _scrap_opening_minutes_prices(symbol: str, start:datetime.datetime, end:datetime.datetime, *, config:Config, metadata:dict = METADATA["minute_prices"]) -> dict:
    """ Scrap the first minutes following earningq. Using yfinance library. """

    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/minute/{start_str}/{end_str}?adjusted=false&sort=desc&limit=120&apiKey={config.polygon_access_key}"

    data = {}

    try:
        res = requests.get(url)
        data = res.json()
    except Exception as e:
        print(f"[ERROR]: Failed to scrap polyugon. \n{e}")

    return data

def _scrap_monthly_prices(symbol:str, start_date:datetime.datetime, end_date:datetime.datetime, metadata:dict = METADATA["monthly_prices"]) -> pd.DataFrame:
    """ Scrap the monthly prices. Using yfinance library. """
    ticker = Ticker(symbol)

    data:pd.DataFrame = ticker.history(start=start_date, end=end_date, interval="1mo", auto_adjust=False, back_adjust=False)

    data = data.drop('Adj Close', axis=1)

    # Renaming as the scrapping is not self made
    data = data.rename(columns=dict(zip(list(data.columns), metadata["columns"][:-1])))
    data.index.name = metadata["index_label"]

    data = data[data["open"].notnull()]
    data["symbol"] = symbol
    data = data.reset_index()

    return data