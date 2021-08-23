import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Youtube Stat Dashboard"

server = app.server
app.config.suppress_callback_exceptions = True