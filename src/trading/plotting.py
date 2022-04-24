
import dash
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from dash import html, dcc
from enum import Enum
from typing import TypeAlias, Callable

from _utils import Data, Array, get_function_name, wrapped_partial

##
#   Data Types Declarations
##
Symbol: TypeAlias = str
class Temporality(Enum):
    WEEK    = 'week'


##
#   Function signature declarations
##
FigurePlot: TypeAlias = Callable[[Symbol, Data], go.Figure] # type: ignore

##
#   Utils Functions
##
def _temporal_reduce(data: Data, _to: Temporality) -> Data:
    """ Reduce the time granularity of the data. """

    # Get the pandas dataframe... 
    # (honestly, that's bad aggregating of arrays is complicated without a Query Language)
    # TODO: Fix the agg, it seems like there is 1 day shifted

    if _to != Temporality.WEEK: raise NotImplementedError("Only WEEK aggregation supported yet. Please retry")

    df = data.df.copy()

    # Remove one week to slide compute for "the week after".
    df.Date = pd.to_datetime(df.Date) - pd.to_timedelta(7, unit='d')

    agg_df = df.resample('W-Mon', on='Date').agg({
        'Open':   'first',
        'High':   'max',
        'Low':    'min',
        'Close':  'last',
        'Volume': 'sum'})

    # Remove the artificially created week
    agg_df = agg_df[agg_df.index > min(df.Date)] #type: ignore

    return Data(agg_df)

##
#   Plotting Functions and Dashboards
##
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
    return dcc.Graph(id = get_function_name(plot_func), figure = plot_func(symbol, data))

def backtest_dashboard(app: dash.Dash, symbol: Symbol, data: Data) -> dash.Dash:
    """ Main dashboard for backtest data. """

    func = wrapped_partial(_plot_line_stock_prices, _key='Close')

    app.layout = html.Div(id= 'container', children = [
        _dashboard_html_title('Backtesting Dashboard'),
        _dashboard_temporal_graph(data, symbol, _plot_candlestick_stock_prices),
        _dashboard_temporal_graph(data, symbol, func)
    ])

    return app