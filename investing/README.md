# Goal

This part of the project attends to explore financial data of the market both present and historic to understand better the stocks and make wiser decision before long-term investiments. Here is a non-exhaustive list:
- Get Tickers for Europe and US Market
- Scrap Financial statements for main tickers
- Detect both stable and growth stocks
- Guess bull and bear market

# Ultimate goal

The ultimate goal of the project is a super architecture able to deploy trading bots over automatic decision and manual triggers.

# TODO

## Features
- Get ticker for US Market and Historicy of tickers
- For each ticker, automate the fetch of required financial data

## Improvments
- Deal with / understand company take over

# Installations

Use the same virtual environment as the other sub projects
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
    pip3 install yfinance
    pip3 install pprinter
    pip3 install beautifulsoup4
    pip3 install requests
    ```