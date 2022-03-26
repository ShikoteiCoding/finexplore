# Finexplore

**Goal**
Understanding finance stock market through data. Better understand investment and dive into trading. Explore Machine Learning opportunities and different long-lasting strategy while trying some innovations.

**Projects Overview**:
- Trading
    - Alerting and daily market recap system
    - Automation buy / sell stocks with different style (day / swing)
- Investing
    - Identify Company with good forecast
    - Browse API with analyst reviews
- Exploration
    - Build dashboard to visualize stock market data
    - Make it interactive to switch between stocks
    - Connect to the stocks from the alerting market recap
    - Connect to the investing data
- General
    - Dockerise trading algorithm + API connectors to run separately
    - Check for kubernetes orchestration

**TODO**:
- Stock & Crypto
    - Identify all macro stock strategies
    - Inside those, find micro strategies (algorithms)
- Exploration
    - Build general-purpose library 

**Dependencies**
- Python3
- Pandas
- Plotly
- Dash (To come)
- Airflow
- Yahoo Finance

**Installation**
- Virtual Environment Setup
    - Create a virtual env in a separate directory
    ```
    virtualenv finance-env
    ```

    - Activate the virtual env
    ```
    source finance-env/bin/activate
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