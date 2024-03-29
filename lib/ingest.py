from psycopg2._psycopg import connection
from psycopg2 import sql
import datetime
import pandas as pd

from config import Config

from scrap import (
    _scrap_daily_prices_for_earnings, 
    _scrap_monthly_prices, 
    _scrap_opening_minutes_prices, 
    _scrap_previous_earnings, 
    _scrap_sp_500_constituents,
    METADATA
)

import utils

#--------------------------
def ingest_sp_500_constituents(connection, *, metadata:dict = METADATA["s&p500"], reload:bool = False) -> None:
    """ 
    Load or scrap the S&P500 constituents and push to the DB. 
    Writing mode is truncating old existing data.
    """
    print(utils.printable_banner("Ingesting S&P500 Constituents."))

    table = "snp_constituents"
    stats = utils.TableStats(connection, table)
    stats.track_table("before_ingestion")

    current_number_constituents = utils.psql_fetch(
        sql.SQL(
            """
            SELECT COUNT(*) AS number
            FROM {table}
            """
        ).format(table=sql.Identifier(table)), connection
    )

    if current_number_constituents["number"][0] == 0 or reload:
        print("\n[INFO]: Fetching S&P500 constituents.")
        constituents = _scrap_sp_500_constituents()
        utils.psql_insert(table, metadata["columns"], utils.dataframe_to_column_dict(constituents), connection, truncate=True)

        stats.track_table("after_ingestion")

    print(f"\n[INFO]: Ingestion statistics are ... \n{stats}")

    return

def ingest_tickers_earnings_history(connection:connection, symbols:list, *, reload:bool = False) -> None:
    """ Scrap the tickers earning history. Upsert the data in the DB. """
    print(utils.printable_banner("Ingesting Earnings History."))
    
    table = "tickers_earnings_history"
    stats = utils.TableStats(connection, table)
    stats.track_table("before_ingestion")

    for symbol in symbols:
        current_earnings = utils.psql_fetch(
            sql.SQL(
                """
                SELECT *
                FROM {table}
                WHERE symbol={symbol}
                """
            ).format(table=sql.Identifier(table), symbol=sql.Literal(symbol))
            , connection
        )
        current_earnings_date =  current_earnings["earnings_date"].unique()
        
        if current_earnings.size == 0 or reload:
            print(f"\n[INFO]: Fetching earnings dates for {symbol}.")
            new_earnings = _scrap_previous_earnings(symbol)
            new_earnings_date = new_earnings["earnings_date"].unique()

            if set([pd.to_datetime(crd).strftime("%Y-%m-%d") for crd in current_earnings_date]) != set([pd.to_datetime(crd).strftime("%Y-%m-%d") for crd in new_earnings_date]):
                # Upsert insert only not existing data.
                # TODO: if data is too big, consider filtering them instead of overloading the DB connection.
                upsert_earnings = utils.psql_upsert_factory(connection, table="tickers_earnings_history", all_columns=list(new_earnings.columns), unique_columns=["earnings_date", "symbol"])
                upsert_earnings(utils.dataframe_to_column_dict(new_earnings, replace_nan=True))

                stats.track_table(f"after_{symbol}_ingestion")

    print(f"\n[INFO]: Ingestion statistics are ... \n{stats}")

    return

def ingest_tickers_daily_prices(
    connection: connection, symbols:list,
    start_date:datetime.datetime, end_date:datetime.datetime,
    *,
    reload:bool = False,
    metadata:dict = METADATA["daily_prices"]) -> None:
    """ Scrap the tickers daily prices and upsert them to the DB """
    print(utils.printable_banner("Ingesting Daily Prices."))

    table = "tickers_daily_share_prices"
    stats = utils.TableStats(connection, table)
    stats.track_table("before_ingestion")

    for symbol in symbols:

        current_daily_prices = utils.psql_fetch(
            sql.SQL(
                """
                SELECT *
                FROM {table}
                WHERE symbol = {symbol};
                """
            ).format(table=sql.Identifier(table), symbol=sql.Literal(symbol)), 
            connection
        )

        # Reload if dates have changed
        if current_daily_prices.size == 0 or reload:
            print(f"\n[INFO]: Fetching new daily shares prices for {symbol}.")

            daily_prices = _scrap_daily_prices_for_earnings(symbol, start_date, end_date)

            upsert_daily = utils.psql_upsert_factory(connection, table="tickers_daily_share_prices", all_columns=list(daily_prices.columns), unique_columns=["date", "symbol"])
            upsert_daily(utils.dataframe_to_column_dict(daily_prices, replace_nan=True))
            
            stats.track_table(f"after_{symbol}_ingestion")

    print(f"\n[INFO]: Ingestion statistics are ... \n{stats}")
    
    return


def ingest_tickers_monthly_prices(
    connection:connection, symbols:list, 
    start_date:datetime.datetime, end_date:datetime.datetime,  
    *, 
    reload:bool = False, 
    metadata:dict = METADATA["monthly_prices"]) -> None:
    """ Scrap the tickers monthly prices and upsert them to the DB. """
    print(utils.printable_banner("Ingesting Daily Prices."))

    table = "tickers_monthly_share_prices"
    stats = utils.TableStats(connection, table)
    stats.track_table("before_ingestion")
    
    for symbol in symbols:
        data = utils.psql_fetch(
            sql.SQL(
                """
                SELECT *
                FROM {table}
                WHERE symbol={symbol};
                """
            ).format(table=sql.Identifier(table), symbol=sql.Literal(symbol)),
            connection
        )

        # TODO: add missing dates to force download (if window bigger than start to end dates)
        if data.size == 0 or reload:
            print(f"\n[INFO]: Fetching new monthly share prices for {symbol}.")

            new_data = _scrap_monthly_prices(symbol, start_date, end_date, metadata)

            upsert = utils.psql_upsert_factory(connection, table="tickers_monthly_share_prices", all_columns=list(new_data.columns), unique_columns=["date", "symbol"])
            upsert(utils.dataframe_to_column_dict(new_data))
            
            stats.track_table(f"after_{symbol}_ingestion")
        
    print(f"\n[INFO]: Ingestion statistics are ... \n{stats}")
    
    return

def ingest_tickers_opening_minute_prices(
    connection:connection, symbols:list, 
    start_date:datetime.datetime, end_date:datetime.datetime,  
    *, 
    config:Config,
    reload:bool = False,
    metadata:dict = METADATA["monthly_prices"]) -> None:
    """ 
    Load minute data from polygon API and push to the DB.  
    """
    print(utils.printable_banner("Ingesting Opening Minute Prices."))

    table = "tickers_minute_share_prices"
    stats = utils.TableStats(connection, table)
    stats.track_table("before_ingestion")
    
    for symbol in symbols:
        data = utils.psql_fetch(
            sql.SQL(
                """
                SELECT * 
                FROM {table} 
                WHERE symbol={symbol};
                """
            ).format(table=sql.Identifier(table), symbol=sql.Literal(symbol)),
            connection
        )

        # TODO: add missing dates to force download (if window bigger than start to end dates)
        if data.size == 0 or reload:
            print(f"\n[INFO]: Fetching new minute share prices for {symbol} between {start_date} and {end_date}.")

            new_data = _scrap_opening_minutes_prices(symbol, start_date, end_date, config=config)
            new_data = utils.polygon_json_to_dataframe(new_data)
            columns = [key for key in new_data[0].keys()]

            upsert = utils.psql_upsert_factory(connection, table="tickers_minute_share_prices", all_columns=columns, unique_columns=["date", "symbol"])
            upsert(new_data)

            stats.track_table("after_ingestion")
        
    print(f"\n[INFO]: Ingestion statistics are ... \n{stats}")
    
    return 