from datapackage import Package
import pandas as pd
import numpy as np
import requests
import datetime

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
    }
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
        print(f"[INFO]: The dataset is empty. Loading the requested symbols")
    
    for symbol in symbols:
        subset = df[df.symbol == symbol]
        
        if subset.size == 0 or reload:
            print(f"[INFO]: Fetching new earnings dates for {symbol}.")
            new_subset = _scrap_previous_earnings(symbol)
            df = df[df.symbol != symbol]
            df = pd.concat([df, new_subset], axis="index", ignore_index=True) # type: ignore

    df.to_csv(file, index_label=metadata["index_label"])

    return df[df.symbol.isin(symbols)] # type: ignore