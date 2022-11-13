# BackTesting Engine

# Build

It is best to encapsulate a dedicated virtual environment. See the documentation for virtualenv: https://virtualenv.pypa.io/en/latest/
```shell
virtualenv venv
source venv/bin/activate
```

Install the dependencies
```shell
pip3 install -r requirements.txt
```

# Run

## Default backtest
```shell
python3 main.py
```

## Custom backtest
- Add your data in the data/companies_stock folder (Or create a crypto_symbol folder and put inside)
- Ensure the columns are at least named after : Date, Close
- Inside the _utils.py file, create a function named after the symbol:
```
    # Make sure the name of the function is the name of the stock / symbol.
    def S&P500(_from: str = "", _to: str = "") -> pd.DataFrame:
        return read_stock("S&P500", _from, _to)
```
- Load the file as in the main.py file
- Run the main.py

# TODO

## Refactor
- Make protocols for Orders as it will depend on the API Broker
- Change dates from str to datetime object (might need a class)
- Responsability of Broker class is too big, find a way to delegate

## Improvements
- Use slots for object performances.
- Implement a full equity (enum ? class ?) instead of max long/short from the broker.
- Implement commision rates
- Convert Trade back to Array Class to Compute Visualization.
- Deal with GTC and IOC Orders:https://www.investopedia.com/terms/g/gtc.asp, https://www.investopedia.com/terms/i/immediateorcancel.asp

## Features
- Dockerize for deployment
- ML
- Add visualization:
    - Should be compatible with Real Time
    - Should serve a web page
    - Add a "vis" mode and "RT" mode to the backtest class




# Conventions

## Classes

- Class Attributes should be named as follows:
    - No underscore: Never
    - Single Underscore:
        - If keyword needed at init (init = True)
        - If keyword not always needed at initialisation (init = False)
    - Double Underscore : If private (init = False)
- Create properties without underscore to secure data access and protect demeter's law
    - Properties for each accessible class attribute
    - Never get_ or set_ methods
- Class Methods should be named as follows:
    - No underscore: Public methods
        - For properties
        - For common methods
    - Single underscore: Never (Because a method is either public or private)
    - Double Underscore: Private methods
- Function input should be named as follow:
    - No underscore: mandatory arguments
    - Single underscore : non-mandatory arguments. To be used in partial
    - Double underscore : No need yet