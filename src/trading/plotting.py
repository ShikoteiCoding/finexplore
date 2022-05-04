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
    return go.Bar(x=data.Date, y=data.Volume, showlegend=showlegend, name=name)

def _equity_line(data: Data, showlegend: bool, name: str = 'Equity') -> go.Scatter: # type: ignore 
    return go.Scatter(x = data.Date, y = data.equity, 
            line = dict(color = 'firebrick', width = 1), 
            showlegend=showlegend, name=name)

##
#   Plotly Graph Object Figures Primitives
##

def _subplot_ohlc_grid(nrows: int, ncols: int) -> go.Figure:  # type: ignore
    """ To combine figures """ 
    return make_subplots(rows=nrows, cols=ncols, shared_xaxes=True, 
               vertical_spacing=0.03, 
               row_width=[0.2, 0.2, 0.6])


##
#   Dash HTML
##
def _dashboard_html_title(title: str) -> html.H1:
    """ HTML for a dashboard title. <H1>. """
    return html.H1(id = 'H1', children = title, style = {'textAlign':'center', 'marginTop':40,'marginBottom':40, 'color':'white'})

def _dashboard_ohlc_graph(app: Dash, symbol: Symbol, data: Data, input: Input) -> dcc.Graph:
    """ Return HTML For callback OHLC Plot. """

    graph_id = "ohlc_graph"

    # This callback is just for reference, it might be deleted
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

    app.layout = html.Div(
        id='dark-theme-components', 
        children = html.Div([
            _dashboard_html_title('Backtesting Dashboard'),
            dcc.Checklist(
                id='toggle-details',
                options=[{'label': 'Show Details', 'value': 'details'}],
                value=['details']
            ),
            _dashboard_ohlc_graph(app, symbol, data, _input)
        ], 
        style={
            'border': 'solid 1px #A2B1C6',
            'border-radius': '5px',
            'padding': '50px',
            'margin-top': '20px',
            'backgroundColor': '#3D3D3D'
        })
    )

    return app