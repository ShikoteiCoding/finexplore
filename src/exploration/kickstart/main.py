import utils
import pandas as pd
import datetime
import yfinance as yf
import matplotlib.pyplot as plt


if __name__ == "__main__":
    
    mmm = yf.Ticker("MMM")
    
    data = mmm.history(start="2022-07-28", end="2022-07-29", interval="1m")