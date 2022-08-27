import utils
import utils
import psycopg2
import dotenv
import requests
from psycopg2 import sql
import json

from config import load_config as load, load_db_opts, load_polygon_opts

if __name__ == "__main__":
    # Load local dotenv (because not dockerize for now - can be added to image or passed at docker run)
    dotenv.load_dotenv(utils.ENV_DOCKER_FILE)
    dotenv.load_dotenv(utils.ENV_SECRETS_FILE)
    config = load(load_db_opts, load_polygon_opts)

    #connection = utils.psql_connect(config)

    tickers = ["MMM"]
    #print(utils._scrap_opening_minutes_earning_date(tickers[0], datetime.datetime(2022, 7, 26), datetime.datetime(2022, 7, 26)))
    print(config)

    url = f"https://api.polygon.io/v2/aggs/ticker/MMM/range/1/minute/2022-07-26/2022-07-26?adjusted=false&sort=asc&limit=120&apiKey={config.polygon_access_key}"

    
    file = "data/test.txt"
    #with open(file, "w") as f:
    #    res = requests.get("https://api.polygon.io/v2/aggs/ticker/MMM/range/1/minute/2022-07-26/2022-07-26?adjusted=false&sort=asc&limit=120&apiKey=KFogwckHT4l3GcS4f7IZEjwbO6DRg_3a")
    #    json_object = json.dumps(res.json(), indent=4)
    #    f.write(json_object)
    print(url)

    #connection.close()