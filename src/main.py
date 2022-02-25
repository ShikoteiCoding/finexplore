import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class Reader:
    
    stocks = ['AAPL', 'IBM', 'MSFT']
    DATA_PATH = 'data/companies_stock'

    def __init__(self, stockName):
        self.dataset = pd.read_csv(Reader.DATA_PATH + '/' + stockName + '.csv')
        self.daily_variation()

    def daily_variation(self):
        self.dataset["daily_variation"] = self.dataset["Close"] - self.dataset["Open"]

    def get_dataset(self):
        return self.dataset
    

if __name__ == '__main__':

    aapl = Reader('AAPL').get_dataset()

    #fig = px.line(
    #    x = aapl["Date"],
    #    y = aapl["Close"]
    #)

    #fig.show()

    fig = go.Figure(go.Candlestick(
        x = aapl.Date,
        open = aapl.Open,
        close = aapl.Close,
        low = aapl.Low,
        high = aapl.High
    ))

    fig.update_layout(
        title = "AAPL Stocks"
    )

    fig.show()