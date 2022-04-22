import dash
from dash import html
from dash import  dcc
import plotly.graph_objects as go
import plotly.express as px

from _utils import Data, Array

def stock_prices(index: Array, serie: Array) -> go.Figure:  # type: ignore
    """ Main stock price vis. """

    fig = go.Figure([go.Scatter(x = index, y = serie,\
                     line = dict(color = 'firebrick', width = 4), name = serie.name)
                     ])
    fig.update_layout(title = 'Prices over time',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Prices'
                      )
    return fig  

def dashboard(data: Data) -> dash.Dash:
    app = dash.Dash()

    app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),

        
        dcc.Graph(id = 'line_plot', figure = stock_prices(data.Date, data.Close))    
    ])

    return app