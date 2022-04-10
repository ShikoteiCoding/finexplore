# TODO

## Data classes to add for organisation
- Order class as an API wrapper to communicate with the broker
- Trade class as a past trade memory.

## Refactor
- Make protocols for Orders as it will depend on the API Broker

## Improvments
- Integrate commition rate to computes
- Data Class and Array Class (as a numpy extend) for performances
- Convert Trade back to Array Class to compute visualization

## Features
- Dockerize for deployment
- ML

# Installation
- Virtual Environment Setup
    - Create a virtual env in a separate directory
    ```
    virtualenv finance-env
    ```

    - Activate the virtual env
    ```
    source finance-env/bin/activate
    ```

    - Go to the src repo
    ```
    cd src/trading
    ```
    
- Dependencies Installation (Update python version)
    ```
    pip3 install pandas
    pip3 install plotly
    pip3 install apache-airflow
    pip3 install python-dotenv
    pip3 install yfinance
    pip3 install alpaca_trade_api
    ```

# Run a backtest
- Add your data in the data/companies_stock folder (Or create a crypto_symbol folder and put inside)
- Ensure the columns are at least named after : Date, Close
- Inside the _utils.py file, create a function named after the symbol:
```
    # Make sure the name of the function is the name of the stock / symbol.
    def S&P500(_from: str = "", _to: str = "") -> pd.DataFrame:
        return read_stock("S&P500", _from, _to)
```
- Load the file as in the main.py file