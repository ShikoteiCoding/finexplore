import dash
from dash import html
from dash import  dcc
import plotly.graph_objects as go
import plotly.express as px

from _utils import Data


def plot(data: Data) -> None:
    app = dash.Dash()

    return app