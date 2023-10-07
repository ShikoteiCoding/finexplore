import pandas as pd
import requests

url = "https://www.financecharts.com/stocks/AAPL/growth/free-cash-flow"

class Ticker:

    def __init__(self, symbol: str):
        self.symbol = symbol

        self.__base_url = "https://www.financecharts.com/stocks/{symbol}/growth/{endpoint}"
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
        }

    
    def free_cash_flow_history(self) -> pd.DataFrame:
        endpoint = "free-cash-flow"

        url = self.__base_url.format(symbol=self.symbol, endpoint=endpoint)

        req = requests.get(url)#, headers=self.__headers)

        print(req.content)

        return pd.DataFrame()

        

if __name__ == "__main__":

    t = Ticker("AAPL")

    t.free_cash_flow_history()