import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Trendboard: Your tool for analyzing social media trends"

server = app.server
app.config.suppress_callback_exceptions = True