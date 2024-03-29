
import psycopg2
import dotenv
import requests
from psycopg2 import sql
import json
import datetime

import utils
import ingest
from config import load_config as load, load_db_opts, load_polygon_opts

if __name__ == "__main__":
    # Load local dotenv (because not dockerize for now - can be added to image or passed at docker run)
    dotenv.load_dotenv(utils.ENV_DOCKER_FILE)
    dotenv.load_dotenv(utils.ENV_SECRETS_FILE)
    config = load(load_db_opts, load_polygon_opts)

    connection = utils.psql_connect(config)

    tickers = ["MSFT"]

    start = datetime.datetime(2022, 7, 26)
    end = datetime.datetime(2022, 7, 26)

    #data = utils._scrap_opening_minutes_earning_date(tickers[0], start, end, config=config)
    #print(utils.polygon_json_to_dataframe(data))

    #data = utils.first_protocol(connection, tickers, reload=True)

    reload = False
    
    ingest.ingest_sp_500_constituents(connection, reload=reload)
    ingest.ingest_tickers_earnings_history(connection, tickers, reload=reload)
    ingest.ingest_tickers_daily_prices(connection, tickers, start, end, reload=reload)
    ingest.ingest_tickers_monthly_prices(connection, tickers, start, end, reload=reload)
    ingest.ingest_tickers_opening_minute_prices(connection, tickers, start, end, config=config, reload=reload)

    connection.close()