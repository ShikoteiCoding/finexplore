import utils

if __name__ == "__main__":

    df = utils.load_ticker_earnings_history(["MMM", "AAPL", "MSFT"], reload=False)
    print(df)