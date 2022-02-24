import pandas as pd
import plotly.express as px

class Reader:
    
    stocks = ['AAPL', 'IBM', 'MSFT']
    DATA_PATH = 'data/companies_stock'

    def __init__(self, stockName):
        self.dataset = pd.read_csv(Reader.DATA_PATH + '/' + stockName + '.csv')

    def get_dataset(self):
        return self.dataset
    

if __name__ == '__main__':

    aapl = Reader('AAPL').get_dataset()

    fig = px.line(
        x = aapl["Date"],
        y = aapl["Volume"]
    )

    fig.show()