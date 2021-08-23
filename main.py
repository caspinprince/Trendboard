import os
from dotenv import load_dotenv
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
    df.columns = ['Publish Date', 'Video Title', 'Description', 'Channel',
                  'Tags', 'Category ID', 'Views', 'Likes', 'Dislikes', 'Comments']
    df['Trending Rank'] = df.index+1
    df = df.convert_dtypes()
    df['Publish Date'] = pd.to_datetime(df['Publish Date'])
    df[['Category ID', 'Views',
        'Likes', 'Dislikes', 'Comments']] = df[['Category ID', 'Views',
                                                'Likes', 'Dislikes', 'Comments']].apply(pd.to_numeric)
    return df

df = getData(50)
plotType = {'Scatterplot': ['Views', 'Likes', 'Dislikes', 'Comments', 'Trending Rank'],
            'Barplot': ['Video Title', 'Channel', 'Category ID'], 'Countplot': ['Channel', 'Category ID']}

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
                                for stat in df.columns[6:]
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
                        html.Button('Refresh', id='refresh', n_clicks=0, className="button"),
                    ],
                    className="menu-item"
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
    [Output("x-axis", "options"),
     Output("y-axis", "disabled"),
     Output("y-axis", "value")],
    Input("graph-type", "value"),
)
def set_options(graph_type):
    options = [
        {"label": stat, "value": stat}
        for stat in plotType[graph_type]
    ]
    disabled, value = (True, None) if graph_type == 'Countplot' else (False, 'Views')
    return options, disabled, value

@app.callback(
    Output("chart", "figure"),
    Input("refresh", "n_clicks"),
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
        chart = px.scatter(df, x=x_stat, y=y_stat, title=f'{x_stat} vs {y_stat} for the Top {numvideos} Trending Videos on Youtube',
                           hover_name='Video Title', hover_data=['Channel'], color='Trending Rank', height=800)
    elif graph_type == 'Countplot':
        chart = px.bar(df, x=df[x_stat].unique(), y=df[x_stat].value_counts(),
                       title = f'Number of Videos by {x_stat} for the Top {numvideos} Trending Videos on Youtube',
                       height=800, labels={'x': x_stat, 'y': 'Videos'})
    else:
        chart = px.bar(df, x=x_stat, y=y_stat, title=f'{x_stat} vs {y_stat} for the Top {numvideos} Trending Videos on Youtube',
                       hover_name='Video Title', hover_data=['Channel'], height=800)
    return chart


if __name__ == "__main__":
    app.run_server(debug=True)
