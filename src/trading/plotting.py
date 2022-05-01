
from xxlimited import Str
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import html, dcc, Input, Output, Dash
from enum import Enum
from typing import ParamSpec, TypeAlias, Callable, Tuple

from _utils import Data, get_function_name, wrapped_partial

##
#       General Plotly to Dash logic:
#
#
#        Plotly Graph Object CLass
#                   |
#                   |
#     Plotly Graph Object Figure Class
#                   |
#                   |
#             Dash dcc Graph
#                   |
#                   |
#             Dash html Div
#
##

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
#   Plotly Graph Object Charts Primitives
##
def _ohlc_candlesticks(data: Data, name: str = 'OHLC') -> go.Candlestick: # type: ignore
    return go.Candlestick(
        x = data.Date, 
        open = data.Open,
        high = data.High,
        close = data.Close,
        low = data.Low,
        name = name
    )

def _volume_bar(data: Data, showlegend: bool, name: str = 'Volume') -> go.Bar: # type: ignore
    return go.Bar(x = data.Date, y = data.Volume, showlegend = showlegend, name = name)

def _equity_line(data: Data, showlegend: bool, name: str = 'Equity') -> go.Scatter: # type: ignore 
    return go.Scatter(x = data.Date, y = data.equity, line = dict(color = 'firebrick', width = 1), showlegend=showlegend, name=name)

##
#   Plotly Graph Object Figures Primitives
##
def _plot_ohlc_candlesticks(symbol: Symbol, data: Data, _has_slider: str = 'slider') -> go.Figure: # type: ignore
    """ Figure for ticked stock prices curve. """
    fig = go.Figure(_ohlc_candlesticks(data, 'OHLC'))

    fig.update_layout(
        title = f'OHLC Plot: {symbol}',
        xaxis_title = data.Date.name,
        yaxis_title = 'Price Cnandlesticks',
        xaxis_rangeslider_visible='slider' in _has_slider
    )
    return fig

def _plot_volume_bar(symbol: Symbol, data: Data) -> go.Figure: # type: ignore
    """ Figure for volumes """
    fig = go.Figure(_volume_bar(data, False))

    return fig

def _subplot_ohlc_grid(nrows: int, ncols: int) -> go.Figure:  # type: ignore
    """ To combine figures """ 
    return make_subplots(rows=nrows, cols=ncols, shared_xaxes=True, 
               vertical_spacing=0.03, 
               row_width=[0.2, 0.2, 0.6])

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
#   Dash HTML
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

def _dashboard_ohlc_graph(app: Dash, symbol: Symbol, data: Data, input: Input) -> dcc.Graph:
    """ Return HTML For callback OHLC Plot. """

    graph_id = "ohlc_graph"

    @app.callback(Output(graph_id, "figure"), input)
    def __figure_update(_input: list):
        """ 
        Update Logic here. 
        Carefull, whole figure need to be created and returned here.
        Function is called on each linked input change in value.
        Cross inputs need to be managed in this single function.
        Only the input list is accepted as the update value.
        """
        fig = _subplot_ohlc_grid(3, 1)

        fig.add_trace(
            _ohlc_candlesticks(data, 'OHLC'),
            row=1, col=1
        )

        if 'details' in _input:
            fig.add_trace(
                _volume_bar(data, True),
                row=2, col=1
            )
            fig.add_trace(
                _equity_line(data, True),
                row=3, col=1
            )

        fig.update(layout_xaxis_rangeslider_visible=False)
        return fig

    return dcc.Graph(id=graph_id)


def backtest_dashboard(app: Dash, symbol: Symbol, data: Data) -> Dash:
    """ Main dashboard for backtest data. """

    # Useless later, let it as a reference on know-how-to
    _input = Input("toggle-details", "value")

    app.layout = html.Div(id= 'container', children = [
        _dashboard_html_title('Backtesting Dashboard'),
        dcc.Checklist(
            id='toggle-details',
            options=[{'label': 'Show Details', 'value': 'details'}],
            value=['details']
        ),
        _dashboard_ohlc_graph(app, symbol, data, _input)
    ])

    return app