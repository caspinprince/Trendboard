import os
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Output, Input

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

def getData():
    request = youtube.videos().list(
        part ='snippet, statistics',
        chart='mostPopular',
        maxResults = 50,
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
    df['Rank'] = df.index+1
    return df


df = getData()
df = df.convert_dtypes()
df['Publish Date'] = pd.to_datetime(df['Publish Date'])
df[['Category ID', 'Views',
    'Likes', 'Dislikes', 'Comments']] = df[['Category ID', 'Views',
                                            'Likes', 'Dislikes', 'Comments']].apply(pd.to_numeric)


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
    [
        Input("x-axis", "value"),
        Input("y-axis", "value"),
    ],
)
def update_charts(x_stat, y_stat):
    chart = px.scatter(df, x=x_stat, y=y_stat, title=f'{x_stat} vs {y_stat}', hover_name='Title',
                        hover_data=['Channel'], color='Rank')
    return chart

if __name__ == "__main__":
    app.run_server(debug=True)
