import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Output, Input, State
from io import BytesIO
import base64
from utilities.youtubedata import getData, get_wordcloud
from app import app

plotType = {'Scatterplot': ['Views', 'Likes', 'Dislikes', 'Comments', 'Trending Rank'],
            'Barplot': ['Video Title', 'Channel', 'Category ID'], 'Countplot': ['Channel', 'Category ID'], 'Wordcloud':[]}

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Youtube Statistic Dashboard", className="header-title",),
                html.P(
                    children="Analyze statistics of Youtube videos and channels using charts and graphs!",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Graph Type", className="menu-title"),
                        dcc.Dropdown(
                            id="graph-type",
                            options=[
                                {"label": graphType, "value": graphType}
                                for graphType in plotType
                            ],
                            value="Scatterplot",
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                    className="menu-item"
                ),
                html.Div(
                    children=[
                        html.Div(children="X-Axis", className="menu-title"),
                        dcc.Dropdown(
                            id="x-axis",
                            value="Likes",
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                    className="menu-item"
                ),
                html.Div(
                    children=[
                        html.Div(children="Y-Axis", className="menu-title"),
                        dcc.Dropdown(
                            id="y-axis",
                            value="Views",
                            clearable=False,
                            className="dropdown",
                            options = [
                                {"label": stat, "value": stat}
                                for stat in plotType['Scatterplot']
                            ],
                        ),
                    ],
                    className="menu-item"
                ),
                html.Div(
                    children=[
                        html.Div(children="Number of Videos", className="menu-title"),
                        dcc.Input(
                            id="numvideos",
                            type="number",
                            placeholder="(1-50)",
                            min=1,
                            max=50,
                            step=1,
                            value="50",
                            className="input-box",
                        ),
                    ],
                    className="menu-item"
                ),
                html.Div(
                    children=[
                        html.Button('Search', id='search', n_clicks=0, className="button"),
                    ],
                    className="menu-item"
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    id="youtube-charts",
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)
@app.callback(
    [Output("x-axis", "options"),
     Output("x-axis", "disabled"),
     Output("y-axis", "disabled"),
     Output("y-axis", "value")],
    Input("graph-type", "value"),
)
def set_options(graph_type):
    options = [
        {"label": stat, "value": stat}
        for stat in plotType[graph_type]
    ]
    x_disabled, y_disabled, y_value = False, False, 'Views'
    if graph_type == 'Countplot':
        y_disabled = True
        y_value = None
    if graph_type == 'Wordcloud':
        x_disabled, y_disabled = True, True
        y_value = None
    return options, x_disabled, y_disabled, y_value

@app.callback(
    Output("youtube-charts", "children"),
    Input("search", "n_clicks"),
    [
        State("x-axis", "value"),
        State("y-axis", "value"),
        State("numvideos", "value"),
        State("graph-type", "value"),
    ],
)
def update_charts(n_clicks, x_stat, y_stat, numvideos, graph_type):
    df = getData(numvideos)
    if graph_type == 'Scatterplot':
        children = dcc.Graph(
            figure = px.scatter(df, x=x_stat, y=y_stat, title=f'{x_stat} vs {y_stat} for the Top {numvideos} Trending Videos on Youtube',
                               hover_name='Video Title', hover_data=['Channel'], color='Trending Rank', height=800)
        )
    elif graph_type == 'Countplot':
        children = dcc.Graph(
            figure = px.bar(df, x=df[x_stat].unique(), y=df[x_stat].value_counts(),
                           title = f'Number of Videos by {x_stat} for the Top {numvideos} Trending Videos on Youtube',
                           height=800, labels={'x': x_stat, 'y': 'Videos'})
        )
    elif graph_type == 'Barplot':
        children = dcc.Graph(
            figure = px.bar(df, x=x_stat, y=y_stat, title=f'{x_stat} vs {y_stat} for the Top {numvideos} Trending Videos on Youtube',
                           hover_name='Video Title', hover_data=['Channel'], height=800)
        )
    else:
        img = BytesIO()
        wordcloud = get_wordcloud(df)
        wordcloud.save(img, format='PNG')
        children = [
            html.Div(f'Most Common Topics in the Top {numvideos} Trending Videos on Youtube', className="photo-title"),
            html.Img(
                src='data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode()),
            ),
        ]
    return children
