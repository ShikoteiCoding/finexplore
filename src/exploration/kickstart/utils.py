from datapackage import Package
import pandas as pd
import numpy as np
import requests

DATA_PATH = "data/"

user_agent_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def _scrap_sp_500_constituants() -> pd.DataFrame:
    """ Scrap the S&P 500 constituents. """
    url = 'https://datahub.io/core/s-and-p-500-companies/datapackage.json'

    resource_name = "constituents_csv"
    columns = ["symbol", "company", "sector"]

    package = Package(url)
    resource = package.get_resource(resource_name)
    if resource:
        table = resource.read()
        return pd.DataFrame(table, columns=columns)
    print("[INFO]: Resource is empty. Consider fixing the get_sp_500_constituents() scrapping function.")
    return pd.DataFrame()

def load_sp_500_constituents(reload=False) -> pd.DataFrame:
    """ Load or scrap the S&P500 constituents. """
    filename = "s&p500_constituents.csv"
    if not reload:
        return pd.read_csv(DATA_PATH + filename, header=0)
    constituents = _scrap_sp_500_constituants()
    constituents.to_csv(DATA_PATH + filename)
    return constituents

def _scrap_previous_earnings(symbol) -> pd.DataFrame:
    url = f"https://finance.yahoo.com/calendar/earnings?symbol={symbol}"
    columns = ["symbol", "company", "earning_dates", "eps_estimates", "eps_reported", "surprise_percent"]

    data = requests.get(url, headers=user_agent_headers).text

    df = pd.DataFrame(columns=columns)

    try:
        df = pd.read_html(data)[0]
        df.replace("-", np.nan, inplace=True)
        df['EPS Estimate'] = pd.to_numeric(df['EPS Estimate'])
        df['Reported EPS'] = pd.to_numeric(df['Reported EPS'])
        df.columns = columns
    except ValueError:
        print(f"[INFO]: No available earnings data for {symbol}")
    return df

def load_ticker_earnings_history(symbols: list, reload: bool=False) -> pd.DataFrame:
    """ Load or scrap the tickers earning history. """
    filename = "tickers_earning_histiry.csv"
    columns = ["symbol", "company", "earning_dates", "eps_estimates", "eps_reported", "surprise_percent"]

    df = pd.DataFrame(columns=columns)
    df_size = 0

    # try to Load the existing csv
    # for each symbols, find them in the csv
        # if symbol is too old or does not exist
        # scrap + merge
        # add to subset
    # if changes, write new csv
    # return subset

    try:
        df = pd.read_csv(DATA_PATH + filename)
        df_size = df.size
    except Exception as e:
        print(f"[INFO]: The dataset is empty. Loading the requested symbols")
    
    for symbol in symbols:
        subset = df[df.symbol == symbol]
        
        if subset.size == 0: # or if data too old ?
            subset = _scrap_previous_earnings(symbol)
            df = pd.concat([df, subset], axis=0)

    return df