import os
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Output, Input, State

from googleapiclient.discovery import build

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Youtube Stat Dashboard"

load_dotenv()
api_key = os.getenv('APIKEY')

youtube = build('youtube', 'v3', developerKey=api_key)

def getData(numResults: int):
    request = youtube.videos().list(
        part ='snippet, statistics',
        chart='mostPopular',
        maxResults = numResults,
        regionCode='CA'
    )
    response = request.execute()
    df = pd.json_normalize(response, 'items')
    df = df[['snippet.publishedAt', 'snippet.title',
             'snippet.description', 'snippet.channelTitle',
             'snippet.tags', 'snippet.categoryId',
             'statistics.viewCount', 'statistics.likeCount',
             'statistics.dislikeCount', 'statistics.commentCount']]
    df.columns = ['Publish Date', 'Title', 'Description', 'Channel',
                  'Tags', 'Category ID', 'Views', 'Likes', 'Dislikes', 'Comments']
    df['Trending Rank'] = df.index+1
    df = df.convert_dtypes()
    df['Publish Date'] = pd.to_datetime(df['Publish Date'])
    df[['Category ID', 'Views',
        'Likes', 'Dislikes', 'Comments']] = df[['Category ID', 'Views',
                                                'Likes', 'Dislikes', 'Comments']].apply(pd.to_numeric)
    return df

df = getData(50)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Youtube Statistic Dashboard", className="header-title",),
                html.P(
                    children="Analyze statistics of youtube videos and channels using charts and graphs!",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="X-Axis", className="menu-title"),
                        dcc.Dropdown(
                            id="x-axis",
                            options=[
                                {"label": x_stat, "value": x_stat}
                                for x_stat in df.columns
                            ],
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
                            options=[
                                {"label": y_stat, "value": y_stat}
                                for y_stat in df.columns
                            ],
                            value="Views",
                            clearable=False,
                            className="dropdown",
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
                        html.Button('Refresh', id='refresh', n_clicks=0, className="button"),
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children= dcc.Graph(
                        id="chart"
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    Output("chart", "figure"),
    Input("refresh", "n_clicks"),
    [
        State("x-axis", "value"),
        State("y-axis", "value"),
        State("numvideos", "value"),
    ],
)
def update_charts(n_clicks, x_stat, y_stat, numvideos):
    df = getData(numvideos)
    chart = px.scatter(df, x=x_stat, y=y_stat, title=f'{x_stat} vs {y_stat} for the {numvideos} Top Trending Videos on Youtube',
                       hover_name='Title', hover_data=['Channel'], color='Trending Rank')
    return chart


if __name__ == "__main__":
    app.run_server(debug=True)
