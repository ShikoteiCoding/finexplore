from dataclasses import dataclass, field
from typing import Callable
from psycopg2._psycopg import connection
from psycopg2 import sql
from config import Config

from scrap import (METADATA)

from ingest import (
    ingest_sp_500_constituents, 
    ingest_tickers_earnings_history, 
    ingest_tickers_daily_prices, 
    ingest_tickers_monthly_prices, 
    ingest_tickers_opening_minute_prices
)

import psycopg2
import pandas as pd
import numpy as np
import datetime

#--------------------------
ENV_DOCKER_FILE = "setup.env"
ENV_SECRETS_FILE = "secrets.env"
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

#--------------------------

def printable_banner(text:str, length:int=50) -> str:
    """ Print a beautified banner. """
    assert type(length) == int, "Please length should be an int."

    if len(text) > length:
        length = len(text) + 10
    
    odd = (length - len(text)) % 2

    border = "#" * (((length - len(text)) // 2) + odd - 1)

    output = "\n" + "#" * (length + odd) + "\n" + border + " " + text + " " + border + "\n" + "#" * (length + odd)
    return output

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

def polygon_json_to_dataframe(json:dict) -> list[dict]:
    formatted = []
    results = json["results"]
    symbol = json["ticker"]

    for result in results:
        formatted.append({
            "date": datetime.datetime.fromtimestamp(result["t"] / 1000),
            "open": result["c"],
            "high": result["h"],
            "low": result["l"],
            "close": result["c"],
            "volume": result["v"],
            "dividends": 0,
            "stock_splits": 0,
            "symbol": symbol
        })

    return formatted

#--------------------------

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
        connection: connection,
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
                INSERT INTO {table} AS t ({columns}) VALUES ({placeholder}) ON CONFLICT ({uniq_columns}) DO UPDATE SET {update_clause};
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

            # Currently not much optimization available from psycopg2
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

@dataclass
class TableStats:
    conn: connection
    table: str
    _stats: dict = field(default_factory=dict)
    
    def track_table(self, label:str) -> None:
        res = psql_fetch(sql.SQL(
            """
            SELECT COUNT(*) AS count_
            FROM {table}
            """
        ).format(table=sql.Identifier(self.table)), self.conn)

        self._stats[label] = res["count_"][0]

    @property
    def stats(self) -> dict:
        return self._stats

    def __str__(self) -> str:
        return str(self._stats)


#--------------------------

def first_protocol(connection:connection, symbols:list, n_last_releases=15, reload=False) -> pd.DataFrame:
    """ Encapsulate the transformations needed for the dataframe to perform analysis. """

    ingest_tickers_earnings_history(connection, symbols, reload=reload)
    ingest_tickers_daily_prices(connection, symbols, start_date=datetime.datetime(1998, 1, 1), end_date=datetime.datetime.now(), reload=reload)
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
        WITH daily_prices AS (
            SELECT
                symbol,
                date,
                open,
                close,
                high,
                low,
                LAG(date, 1) OVER (PARTITION BY symbol ORDER BY date DESC) AS next_date
            FROM tickers_daily_share_prices
            WHERE symbol in ({tickers})
        ),
        enriched_earnings AS (
            SELECT
                T.earnings_date,
                to_char(earnings_date, 'Day')   AS earnings_weekday,
                T.symbol,
                P.open              AS open_current_day,
                P.high              AS high_current_day,
                P.low               AS low_current_day,
                P.close             AS close_current_day,
                P1.open             AS open_previous_day,
                P1.high             AS high_previous_day,
                P1.low              AS low_previous_day,
                P1.close            AS close_previous_day,
                T.eps_estimates,
                T.eps_reported,
                T.surprise_percent
            FROM tickers_earnings_history AS T
            LEFT JOIN daily_prices AS P
                ON T.symbol = P.symbol AND DATE_TRUNC('day', T.earnings_date) = DATE_TRUNC('day', P.date)
            LEFT JOIN daily_prices AS P1
                ON T.symbol = P1.symbol AND DATE_TRUNC('day', T.earnings_date) = DATE_TRUNC('day', P1.next_date)
            WHERE TRUE
                AND T.symbol in ({tickers})
                AND T.eps_reported IS NOT NULL
            ORDER BY T.earnings_date DESC
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
                E.eps_estimates,
                E.eps_reported,
                E.surprise_percent,
                E.open_current_day,
                E.close_previous_day,
                P.open,
                P.high,
                CASE
                    WHEN DATE_TRUNC('month', E.earnings_date) = DATE_TRUNC('month', P.date - '1 years'::interval) THEN '1 year'
                    WHEN DATE_TRUNC('month', E.earnings_date) = DATE_TRUNC('month', P.date - '6 months'::interval) THEN '6 months'
                    WHEN DATE_TRUNC('month', E.earnings_date) = DATE_TRUNC('month', P.date - '3 months'::interval) THEN '3 months'
                    ELSE '0'
                END AS trailing_period
            FROM enriched_earnings AS E
            LEFT JOIN prices AS P
                ON E.symbol = P.symbol AND DATE_TRUNC('day', P.date) <= DATE_TRUNC('day', E.earnings_date) --BETWEEN E.earnings_date - '1 years'::interval AND E.earnings_date
            WHERE E.eps_reported IS NOT NULL
        ),
        grouped AS (
            SELECT
                symbol,
                earnings_date,
                to_char(earnings_date, 'Day')   AS earnings_weekday,
                open_current_day,
                close_previous_day,
                eps_estimates,
                eps_reported,
                surprise_percent,
                MAX(high)                       AS all_time_trailing_max,
                MAX(open) FILTER (WHERE trailing_period = '1 year') AS yty_tendency
            FROM trailing_prices
            GROUP BY
                symbol,
                earnings_date,
                open_current_day,
                close_previous_day,
                eps_estimates,
                eps_reported,
                surprise_percent
            ORDER BY earnings_date DESC
        )
        SELECT *
        FROM grouped
        """
    ).format(
        tickers=sql.SQL(',').join(
            [sql.Literal(ticker) for ticker in symbols]
        )
    )
    return psql_fetch(query, connection)