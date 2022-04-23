from functools import partial
from typing import TypeAlias, Callable
import dash
from dash import html
from dash import  dcc
import plotly.graph_objects as go
import plotly.express as px

from _utils import Data, Array

##
#   Data Types Declarations
##
Symbol: TypeAlias = str

##
#   Function signature declarations
##
FigurePlot: TypeAlias = Callable[[Symbol, Data], go.Figure] # type: ignore

def _plot_candlestick_stock_prices(symbol: Symbol, data:Data) -> go.Figure: # type: ignore
    """ Figure for ticked stock prices curve. """
    fig = go.Figure([go.Candlestick(
        x = data.Date, 
        open = data.Open,
        high = data.High,
        close = data.Close,
        low = data.Low,
        name = 'Candle')])
    fig.update_layout(
        title = f'Prices of symbol: {symbol}',
        xaxis_title = data.Date.name,
        yaxis_title = 'Price sticks'
    )
    return fig

def _plot_line_stock_prices(symbol: Symbol, data: Data, _key: str) -> go.Figure:  # type: ignore
    """ Figure for stock prices curve. """
    index = data.Date
    serie = data[_key] or data.Close # default

    fig = go.Figure([go.Scatter(x = index, y = serie, line = dict(color = 'firebrick', width = 4), name = f'{serie.name} Line plot')])
    fig.update_layout(
        title = f'Prices of symbol: {symbol}',
        xaxis_title = index.name,
        yaxis_title = serie.name
    )
    return fig

def _dashboard_html_title(title: str) -> html.H1:
    """ HTML for a dashboard title. <H1>. """
    return html.H1(id = 'H1', children = title, style = {'textAlign':'center', 'marginTop':40,'marginBottom':40})

def _dashboard_temporal_graph(data: Data, symbol: Symbol, plot_func: FigurePlot) -> dcc.Graph:
    """ HTML for a dashboard graph. """
    return dcc.Graph(id = 'line_plot', figure = plot_func(symbol, data))

def backtest_dashboard(app: dash.Dash, symbol: Symbol, data: Data) -> dash.Dash:
    """ Main dashboard for backtest data. """

    #func = partial(_plot_line_stock_prices, _key='Close')

    app.layout = html.Div(id= 'container', children = [
        _dashboard_html_title('Backtesting Dashboard'),
        _dashboard_temporal_graph(data, symbol, _plot_candlestick_stock_prices)
    ])

    return app