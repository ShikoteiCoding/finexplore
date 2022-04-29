
from functools import partial
from pyclbr import Function
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from dash import html, dcc, Input, Output, Dash
from enum import Enum
from typing import Any, Concatenate, ParamSpec, TypeAlias, Callable, Optional, Union

from _utils import Data, Array, get_function_name, wrapped_partial

##
#   Data Types Declarations
##
Symbol: TypeAlias = str
Kwargs = ParamSpec('Kwargs')


class Temporality(Enum):
    WEEK    = 'week'


##
#   Function signature declarations
##
SimpleFigurePlot: TypeAlias = Callable[[Symbol, Data], go.Figure] # type: ignore
ComplexFigurePlot: TypeAlias = Callable[[Symbol, Data, str], go.Figure] # type: ignore

#FigurePlot: TypeAlias = Union[SimpleFigurePlot, ComplexFigurePlot]

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
    agg_df['Date'] = agg_df.index

    return Data(agg_df)

##
#   Plotting Functions and Dashboards
##
def _plot_ohlc_stock_prices(symbol: Symbol, data: Data, _has_slider: str = 'slider') -> go.Figure: # type: ignore
    """ Figure for ticked stock prices curve. """
    fig = go.Figure(go.Candlestick(
        x = data.Date, 
        open = data.Open,
        high = data.High,
        close = data.Close,
        low = data.Low,
        name = 'OHLC Plot'))
    fig.update_layout(
        title = f'OHLC Plot: {symbol}',
        xaxis_title = data.Date.name,
        yaxis_title = 'Price sticks',
        xaxis_rangeslider_visible='slider' in _has_slider
    )
    return fig

def _plot_bar_stock_volume(symbol: Symbol, data: Data) -> go.Figure: # type: ignore
    """ Figure for volumes """
    fig = go.Figure(go.Bar(x = data.Date, y=data.Volume, showlegend=False))

    return fig

def _plot_line_stock_prices(symbol: Symbol, data: Data, _key: str = 'Close') -> go.Figure:  # type: ignore
    """ Figure for stock prices curve. """
    index = data.Date
    serie = data[_key]

    fig = go.Figure([go.Scatter(x = index, y = serie, line = dict(color = 'firebrick', width = 4), name = f'{serie.name} Line plot')])
    fig.update_layout(
        title = f'Prices of symbol: {symbol}',
        xaxis_title = index.name,
        yaxis_title = serie.name
    )
    return fig

##
#   HTML Functions
##
def _dashboard_html_title(title: str) -> html.H1:
    """ HTML for a dashboard title. <H1>. """
    return html.H1(id = 'H1', children = title, style = {'textAlign':'center', 'marginTop':40,'marginBottom':40})

def _dashboard_temporal_graph(data: Data, symbol: Symbol, plot_func: SimpleFigurePlot) -> dcc.Graph:
    """ HTML for a dashboard graph. """
    return dcc.Graph(id = get_function_name(plot_func), figure = plot_func(symbol, data))

def _dashboard_callback_graph(app: Dash, data: Data, symbol: Symbol, plot_func: ComplexFigurePlot, input: Input) -> dcc.Graph:
    """ Return HTML for a callback function. """

    graph_id = get_function_name(plot_func)

    @app.callback(Output(graph_id, "figure"), input)
    def _callback_plot_candlestick(_input: str):
       return plot_func(symbol, data, _input)

    return dcc.Graph(id=graph_id)


def backtest_dashboard(app: Dash, symbol: Symbol, data: Data) -> Dash:
    """ Main dashboard for backtest data. """

    line_stock_func = wrapped_partial(_plot_line_stock_prices, _key='Close')

    weekly_data = _temporal_reduce(data, Temporality.WEEK)

    _input = Input("toggle-rangeslider", "value")

    app.layout = html.Div(id= 'container', children = [
        _dashboard_html_title('Backtesting Dashboard'),
        dcc.Checklist(
            id='toggle-rangeslider',
            options=[{'label': 'Include Rangeslider', 'value': 'slider'}],
            value=['slider']
        ),
        _dashboard_callback_graph(app, weekly_data, symbol, _plot_ohlc_stock_prices, _input),
        _dashboard_temporal_graph(weekly_data, symbol, _plot_bar_stock_volume),
        _dashboard_temporal_graph(data, symbol, line_stock_func)
    ])

    return app