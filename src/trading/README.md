**TODO**

- Data class (Data Mapper Needed ?)
- Order class   ->
- Trade class   -> Broker can store all the past trades. Responsible for writing outputs.

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