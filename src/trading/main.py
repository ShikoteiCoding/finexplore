from dotenv import load_dotenv
from pathlib import Path
import os
import yfinance

if __name__ == '__main__':
    # Running the env file
    load_dotenv(dotenv_path = 'setup.env')

    # Loading Env Variables
    ALPACA_USER = os.getenv('ALPACA_USER')
    ALPACA_PWD  = os.getenv('ALPACA_PWD')

