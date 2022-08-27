from typing import Callable, Optional
from datapackage import Package
import pandas as pd
import numpy as np
import requests
import datetime
from yfinance import Ticker
import psycopg2


#--------------------------
ENV_FILE = "setup.env"
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
METADATA = {
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
        "filename": "tickers_monthly_share_prices.csv",
        "columns": ["open", "high", "low", "close", "volume", "dividends", "stock_splits", "symbol"],
        "index_label": "date"
    },
}
#--------------------------

def str_to_hour(hour:str, format:str = "%H:%M") -> datetime.time:
    return datetime.datetime.strptime(hour, format).time()

def dataframe_to_column_dict(df:pd.DataFrame, replace_nan:bool = False) -> list[dict]:
    """ Utility function to build a list of rows with column name as key. """
    data = []
    for _, row in df.iterrows():
        if not replace_nan:
            data.append(row.to_dict())
        else:
            data.append(row.replace({np.nan: None}).to_dict())

    return data

#--------------------------
from psycopg2._psycopg import connection
from psycopg2 import sql
from config import Config

class DBConnectionError(Exception):
    ...

def psql_connect(config: Config) -> connection:
    """ Establish a connection with psycopg2 and the database. """

    try:
        connection = psycopg2.connect(
            database=config.db_name,
            user=config.db_username,
            password=config.db_password,
            host=config.db_host,
            port=config.db_port
        )
    except Exception as e:
        raise DBConnectionError(f"Error: Please verify the connection provided, {e}")
    return connection

def psql_fetch(query:sql.Composed | sql.SQL, connection:connection) -> pd.DataFrame:
    """ Execute a select query and return a dataframe with expected data. """

    # Make it stronger later on through the use of po
    #assert "SELECT" in query, "The query is not a selection."

    cursor = connection.cursor()
    cursor.execute(query=query)

    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    # TODO: add the columns to the dataframe

    return pd.DataFrame(data, columns=columns)

def psql_insert(table:str, columns, data:list, connection:connection, *, truncate=False) -> None:
    """ Execute a query and return a dataframe with expected data. """
    query = sql.SQL(
        """
        INSERT INTO {table} ({columns}) VALUES ({placeholder});
        """
    ).format(
        table=sql.Identifier(table),
        columns=sql.SQL(",").join([sql.Identifier(c) for c in columns]),
        placeholder=sql.SQL(",").join(
            [sql.Placeholder(c) for c in columns]
        )
    )

    cursor = connection.cursor()

    try:

        if truncate:
            cursor.execute(sql.SQL("TRUNCATE {table}").format(table=sql.Identifier(table)))

        if len(data) > 1:
            cursor.executemany(query, data)
        elif len(data) == 1:
            cursor.execute(query, data[0])
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

    return

# Define Function Signature
UpdateClauseFunction = Callable[[list[str]], sql.Composed]

def default_update_clause(update_columns: list[str]) -> sql.Composed:
    update_clause = sql.SQL(",").join(
        [
            sql.Composed(
                [
                    sql.Identifier(c),
                    sql.SQL("= EXCLUDED."),
                    sql.Identifier(c),
                ]
            )
            for c in update_columns
        ]
    )
    return update_clause


def psql_upsert_factory(
        connection: connection, #db_host: str, db_name: str, db_username: str, db_password: str, db_port: str,
        *,
        table: str, all_columns: list[str], unique_columns: list[str], 
        update_clause_func: UpdateClauseFunction = default_update_clause
    ):
    
    def upsert(data:list[dict]):
        cursor = None
        try:
            cursor = connection.cursor()
            update_columns = [
                col_name for col_name in all_columns if col_name not in unique_columns
            ]

            query = sql.SQL(
                """
                INSERT INTO {table} AS t ({columns}) VALUES ({placeholder}) ON CONFLICT ({uniq_columns}) DO UPDATE SET {update_clause}
                """
            ).format(
                table=sql.Identifier(table),
                columns=sql.SQL(",").join([sql.Identifier(c) for c in all_columns]),
                placeholder=sql.SQL(",").join(
                    [sql.Placeholder(c) for c in all_columns]
                ),
                uniq_columns=sql.SQL(",").join(
                    [sql.Identifier(c) for c in unique_columns]
                ),
                update_clause=update_clause_func(update_columns),
            )

            for row in data:
                cursor.execute(query, row)
            connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print("UPSERT ERROR:", error)
            if connection is not None:
                connection.rollback()
            raise error
        finally:
            if cursor is not None: cursor.close()

    return upsert

#--------------------------
def _scrap_sp_500_constituents(*, metadata:dict = METADATA["s&p500"]) -> pd.DataFrame:
    """ Scrap the S&P 500 constituents. """

    package = Package("https://datahub.io/core/s-and-p-500-companies/datapackage.json")
    resource = package.get_resource("constituents_csv")

    if not resource:
        print("[INFO]: Resource is empty. Consider fixing the get_sp_500_constituents() scrapping function.")
        return pd.DataFrame()

    return pd.DataFrame(resource.read(), columns=metadata["columns"])
    

def ingest_sp_500_constituents(connection, *, metadata:dict = METADATA["s&p500"]) -> None:
    """ 
    Load or scrap the S&P500 constituents.

    This load overwrite the previously charged data as they are not historicized.
    """
    constituents = _scrap_sp_500_constituents()
    psql_insert("snp_constituents", metadata["columns"], dataframe_to_column_dict(constituents), connection, truncate=True)

    return

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

def ingest_tickers_earnings_history_and_daily_share_prices(connection:connection, symbols:list, *, reload:bool = False, metadata:dict = METADATA["earnings_history"]) -> None:
    """ Scrap the tickers earning history. """

    for symbol in symbols:
        current_earnings = psql_fetch(sql.SQL("SELECT * FROM tickers_earnings_history"), connection)
        
        if current_earnings.size == 0 or reload:
            print(f"[INFO]: Fetching new earnings dates for {symbol}.")
            earnings_history = _scrap_previous_earnings(symbol)
            earnings_date = earnings_history["earnings_date"].unique()
            start_date = pd.to_datetime(earnings_date.min())
            end_date = pd.to_datetime(earnings_date.max())
            daily_prices = _scrap_daily_prices_for_earnings(symbol, start_date, end_date) # type: ignore

            
            upsert_monthly = psql_upsert_factory(connection, table="tickers_earnings_history", all_columns=list(earnings_history.columns), unique_columns=["earnings_date", "symbol"])
            upsert_monthly(dataframe_to_column_dict(earnings_history, replace_nan=True))

            upsert_daily = psql_upsert_factory(connection, table="tickers_daily_share_prices", all_columns=list(daily_prices.columns), unique_columns=["date", "symbol"])
            upsert_daily(dataframe_to_column_dict(daily_prices, replace_nan=True))

    return

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

def ingest_tickers_monthly_prices(
    connection:connection, symbols:list, 
    start_date:datetime.datetime, end_date:datetime.datetime,  
    *, 
    reload:bool = False, 
    metadata:dict = METADATA["monthly_prices"]) -> None:
    """ Scrap the tickers monthly prices. """
    
    for symbol in symbols:
        data = psql_fetch(
            sql.SQL(
                """
                SELECT * FROM tickers_monthly_share_prices WHERE symbol={symbol};
                """
            ).format(symbol=sql.Literal(symbol)),
            connection
        )

        # TODO: add missing dates to force download (if window bigger than start to end dates)
        if data.size == 0 or reload:
            print(f"[INFO]: Fetching new monthly share prices for {symbol}.")

            new_data = _scrap_monthly_prices(symbol, start_date, end_date, metadata)

            upsert = psql_upsert_factory(connection, table="tickers_monthly_share_prices", all_columns=list(new_data.columns), unique_columns=["date", "symbol"])
            upsert(dataframe_to_column_dict(new_data))
    
    return

#--------------------------
def first_protocol(symbols:list, connection:connection, n_last_releases=15, reload=False) -> pd.DataFrame:
    """ Encapsulate the transformations needed for the dataframe to perform analysis. """

    ingest_tickers_earnings_history_and_daily_share_prices(connection, symbols, reload=reload)
    ingest_tickers_monthly_prices(connection, symbols, start_date=datetime.datetime(1998, 1, 1), end_date=datetime.datetime.now(), reload=reload)

    # Load data for each symbols
    # Get the n most recent release per ticker
    # Compute a field to know if next opening is today or following market opening day
    # Compute min /max earnings date per symbol
    # Grep monthly data for all symbol from min_date - 1 year to max earnings_date
    # Add the all time high previous the report
    # Get all the first 30 minutes (1 min interval) after the report in a separate dataframe.
    query = sql.SQL(
        """
        WITH earnings AS (
            SELECT
                *
            FROM tickers_earnings_history
            WHERE symbol in ({tickers})
        ),
        prices AS (
            SELECT * 
            FROM tickers_monthly_share_prices
            WHERE symbol IN ({tickers})
        ),
        trailing_prices AS (
            SELECT
                E.earnings_date,
                E.symbol,
                E.company,
                E.eps_estimates,
                E.eps_reported,
                E.surprise_percent,
                P.high,
                P.open,
                P.close,
                CASE
                    WHEN DATE_TRUNC('month', E.earnings_date) = P.date - '1 years'::interval THEN '1 year'
                    WHEN DATE_TRUNC('month', E.earnings_date) = P.date - '6 months'::interval THEN '6 months'
                    WHEN DATE_TRUNC('month', E.earnings_date) = P.date - '3 months'::interval THEN '3 months'
                END AS trailing_period
            FROM earnings AS E
            LEFT JOIN prices AS P
                ON E.symbol = P.symbol AND P.date BETWEEN E.earnings_date - '1 years'::interval AND E.earnings_date
            WHERE E.eps_reported IS NOT NULL
        )
        SELECT
            symbol,
            company,
            earnings_date,
            company,
            eps_estimates,
            eps_reported,
            surprise_percent,
            MAX(high) AS trailing_max
        FROM trailing_prices
        GROUP BY
            symbol,
            company,
            earnings_date,
            company,
            eps_estimates,
            eps_reported,
            surprise_percent
        """
    ).format(
        tickers=sql.SQL(',').join(
            [sql.Literal(ticker) for ticker in symbols]
        )
    )
    return psql_fetch(query, connection)