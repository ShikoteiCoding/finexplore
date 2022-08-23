from calendar import month
from datapackage import Package
import pandas as pd
import numpy as np
import requests
import datetime
from yfinance import Ticker

#--------------------------

DATA_PATH = "data/"
OPENING_HOURS = {
    "EST": {
        "start": "09:30",
        "end": "16:00"
    },
    "CST": {
        "start": "08:30",
        "end": "15:00"
    },
    "MST": {
        "start": "07:30",
        "end": "14:00"
    },
    "PST": {
        "start": "06:30",
        "end": "13:00"
    }
}
USER_AGENT_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
CSV_METADATA = {
    "s&p500": {
        "filename": "s&p500_constituents.csv",
        "columns": ["symbol","company","sector"],
        "index_label": "index"
    },
    "earnings_history": {
        "filename": "tickers_earnings_history.csv",
        "columns": ["symbol", "company", "earnings_date", "eps_estimates", "eps_reported", "surprise_percent"],
        "index_label": "index"
    },
    "monthly_prices": {
        "filename": "monthly_share_prices.csv",
        "columns": ["open", "high", "low", "close", "volume", "dividends", "stock_splits", "symbol"],
        "index_label": "date"
    },
}
#--------------------------

def str_to_hour(hour:str, format:str = "%H:%M") -> datetime.time:
    return datetime.datetime.strptime(hour, format).time()

#--------------------------

def _scrap_sp_500_constituents(*, metadata:dict = CSV_METADATA["s&p500"]) -> pd.DataFrame:
    """ Scrap the S&P 500 constituents. """

    url = "https://datahub.io/core/s-and-p-500-companies/datapackage.json"
    resource_name = "constituents_csv"
    package = Package(url)
    resource = package.get_resource(resource_name)
    if resource:
        table = resource.read()
        return pd.DataFrame(table, columns=metadata["columns"])
    print("[INFO]: Resource is empty. Consider fixing the get_sp_500_constituents() scrapping function.")
    return pd.DataFrame()

def load_sp_500_constituents(*, reload:bool = False, metadata:dict = CSV_METADATA["s&p500"]) -> pd.DataFrame:
    """ Load or scrap the S&P500 constituents. """

    file = DATA_PATH + metadata["filename"]
    if not reload:
        return pd.read_csv(file, header=0, index_col=metadata["index_label"])
    constituents = _scrap_sp_500_constituents()
    constituents.to_csv(file, index_label=metadata["index_label"])
    return constituents

def _scrap_previous_earnings(symbol:str, *, metadata:dict = CSV_METADATA["earnings_history"]) -> pd.DataFrame:
    """ Scrap the earnings report data from yfinance. """

    # TODO: Improve the scrapping by loading the second page (data are paginated)
    # For now, only works after 1998 (might be enough though)
    url = f"https://finance.yahoo.com/calendar/earnings?symbol={symbol}"
    data = requests.get(url, headers=USER_AGENT_HEADER).text
    df = pd.DataFrame(columns=metadata["columns"])

    try:
        df = pd.read_html(data)[0]
        df.replace("-", np.nan, inplace=True)

        # Consider adding the timezone if needed.
        # PS: opening hour can be infered by min hour of history share prices for a specific day
        df['EPS Estimate'] = pd.to_numeric(df['EPS Estimate'])
        df['Reported EPS'] = pd.to_numeric(df['Reported EPS'])
        df['Earnings Date'] = pd.to_datetime(
            df['Earnings Date'].apply(lambda x: x[:-3]), 
            format="%b %d, %Y, %I %p"
        )
        df.columns = metadata["columns"]
    except ValueError:
        print(f"[INFO]: No available earnings data for {symbol}")
    return df

def load_ticker_earnings_history(symbols:list, *, reload:bool = False, metadata:dict = CSV_METADATA["earnings_history"]) -> pd.DataFrame:
    """ Load or scrap the tickers earning history. """
    file = DATA_PATH + metadata["filename"]
    df = pd.DataFrame(columns=metadata["columns"])

    try:
        df = pd.read_csv(file, index_col=metadata["index_label"], parse_dates=['earnings_date'])
    except Exception as e:
        print(f"[INFO]: The dataset is empty. Loading the requested symbols earnings history.")
    
    for symbol in symbols:
        subset = df[df.symbol == symbol]
        
        if subset.size == 0 or reload:
            print(f"[INFO]: Fetching new earnings dates for {symbol}.")
            new_subset = _scrap_previous_earnings(symbol)
            df = df[df.symbol != symbol]
            df = pd.concat([df, new_subset], axis="index", ignore_index=True) # type: ignore

    df.to_csv(file, index_label=metadata["index_label"])

    return df[df.symbol.isin(symbols)] # type: ignore

def load_monthly_prices(symbols:list, start_date:datetime.datetime, end_date:datetime.datetime, *, reload:bool = False, metadata:dict = CSV_METADATA["monthly_prices"]) -> pd.DataFrame:
    """ Load or scrap the tickers monthly prices. """
    file = DATA_PATH + metadata["filename"]
    df = pd.DataFrame(columns=metadata["columns"])

    try:
        df = pd.read_csv(file, index_col=metadata["index_label"])
    except Exception as e:
        print(f"[INFO]: The dataset is empty. Loading the requested symbols share prices.")
    
    for symbol in symbols:
        subset = df[df.symbol == symbol]
        
        # TODO: add missing dates to force download (if window bigger than start to end dates)
        if subset.size == 0 or reload:
            print(f"[INFO]: Fetching new monthly share prices for {symbol}.")
            ticker = Ticker(symbol)
            new_subset:pd.DataFrame = ticker.history(start=start_date, end=end_date, interval="1mo", auto_adjust=False, back_adjust=False)
            new_subset = new_subset.drop('Adj Close', axis=1)

            # Remove already existing elements
            df = df[df.symbol != symbol]

            # Renaming as the scrapping is not self made
            new_subset = new_subset.rename(columns=dict(zip(list(new_subset.columns), metadata["columns"][:-1])))
            new_subset.index.name = metadata["index_label"]

            new_subset = new_subset[new_subset["open"].notnull()]
            new_subset["symbol"] = symbol

            df = pd.concat([df, new_subset], axis="index", ignore_index=False) # type: ignore

    df.to_csv(file, index_label=metadata["index_label"])

    return df[df.symbol.isin(symbols)] # type: ignore

#--------------------------

def enrich_tickers_earnings_history(df: pd.DataFrame, n_last_release:int = 15) -> pd.DataFrame:
    """ Encapsulate the transformations needed for the dataframe to perform analysis. """

    # Get distinct tickers
    distinct_tickers = df["symbol"].unique()

    # Remove where no estimate
    filtered_earnings = df[df["eps_reported"].notnull()]

    # Get the n most recent release per ticker
    last_n_release_per_ticker = filtered_earnings.sort_values(by=["symbol", "earnings_date"], ascending=False).groupby("symbol").head(n_last_release)

    # Compute a field to know if next opening is today or following market opening day
    last_n_release_per_ticker["day_following_report"] = last_n_release_per_ticker["earnings_date"].apply(
        lambda x: 
        "current_day"
        if (
            datetime.time(x.hour) >= str_to_hour(OPENING_HOURS["EST"]["start"])
            and datetime.time(x.hour) < str_to_hour(OPENING_HOURS["EST"]["end"])
        )
        else "next_day"
    )
    last_n_release_per_ticker["earnings_month"] = last_n_release_per_ticker["earnings_date"] + pd.offsets.MonthBegin(-1) # type: ignore

    # Compute min /max earnings date per symbol
    min_max_dates_per_symbol = filtered_earnings.groupby("symbol").agg({"earnings_date": ["min", "max", "count"]}).droplevel(axis=1, level=0)
    
    # Grep monthly data for all symbol from min_date - 1 year to max earnings_date
    stock_prices = pd.DataFrame()

    for symbol in distinct_tickers:
        start_date = min_max_dates_per_symbol.filter(items=[symbol], axis=0)["min"][0] - pd.DateOffset(years=1)
        end_date = min_max_dates_per_symbol.filter(items=[symbol], axis=0)["max"][0]
        monthly_prices = load_monthly_prices([symbol], start_date=start_date, end_date=end_date)
        monthly_prices["previous_max"] = monthly_prices["high"].cummax()
        
        # TODO: Might be possible to miss months ? In this case, lagging by absolute number might not work
        monthly_prices["open_trend_one_year"] = 100 * (monthly_prices["open"] - monthly_prices["open"].shift(12)) / monthly_prices["open"]
        monthly_prices["open_trend_six_months"] = 100 * (monthly_prices["open"] - monthly_prices["open"].shift(6)) / monthly_prices["open"]
        monthly_prices["open_trend_three_months"] = 100 * (monthly_prices["open"] - monthly_prices["open"].shift(3)) / monthly_prices["open"]

        #print(monthly_prices)
        #stock_prices = pd.concat([stock_prices, monthly_prices]) 

        #symbol_earnings = last_n_release_per_ticker[last_n_release_per_ticker["symbol"] == symbol]

    print(last_n_release_per_ticker)

    # Add the all time high previous the report
    # Get all the first 30 minutes (1 min interval) after the report in a separate dataframe.

    return last_n_release_per_ticker