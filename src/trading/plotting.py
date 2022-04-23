from functools import partial
from typing import TypeAlias, Callable
import dash
from dash import html
from dash import  dcc
import plotly.graph_objects as go
import plotly.express as px

from _utils import Data, Array

Symbol: TypeAlias = str

FigurePlot: TypeAlias = Callable[[Symbol, Array, Array], go.Figure] # type: ignore

def _plot_line_stock_prices(symbol: Symbol, index: Array, serie: Array) -> go.Figure:  # type: ignore
    """ Figure for stock prices curve. """
    fig = go.Figure([go.Scatter(x = index, y = serie, line = dict(color = 'firebrick', width = 4), name = serie.name)])
    fig.update_layout(
        title = f'Prices of symbol: {symbol}',
        xaxis_title = index.name,
        yaxis_title = serie.name
    )
    return fig

def _plot_tick_stock_prices(symbol: Symbol, index: Array, serie:Array) -> go.Figure: # type: ignore
    """ Figure for ticked stock prices curve. """
    fig = go.Figure([go.Scatter(x = index, y = serie, line = dict(color = 'firebrick', width = 4), name = serie.name)])
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
    return dcc.Graph(id = 'line_plot', figure = plot_func(symbol, data.Date, data.Close))

def backtest_dashboard(app: dash.Dash, symbol: Symbol, data: Data) -> dash.Dash:
    """ Main dashboard for backtest data. """

    app.layout = html.Div(id= 'container', children = [
        _dashboard_html_title('Backtesting Dashboard'),
        _dashboard_temporal_graph(data, symbol, _plot_line_stock_prices)
    ])

    return app

def build_stock_prices_tick_curve(app: dash.Dash, data: Data) -> dash.Dash:

    return app