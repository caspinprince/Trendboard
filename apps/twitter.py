import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from app import app
from utilities.twitterdata import getTweets, getCountries, getTrendWordcloud
from io import BytesIO
import base64

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Twitter Statistic Dashboard", className="header-title",),
                html.P(
                    children="Analyze trending topics, tweets and users through the Twitter API!",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Task Type", className="menu-title"),
                        dcc.Dropdown(
                            id="task-type",
                            value="Views",
                            clearable=False,
                            className="dropdown",
                            options = [
                                {"label": option, "value": option}
                                for option in ['Trending Topics', 'Average Sentiment']
                            ],
                        ),
                    ],
                    className="menu-item"
                ),
                html.Div(
                    children=[
                        html.Div(children="Country Filter", className="menu-title"),
                        dcc.Dropdown(
                            id="country-filter",
                            options=[
                                {"label": country, "value": country}
                                for country in getCountries()
                            ],
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                    className="menu-item"
                ),
                html.Div(
                    children=[
                        html.Div(children="Topic Search", className="menu-title"),
                        dcc.Input(
                            id="topic-search",
                            type="text",
                            placeholder="Input a topic here",
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
                    id="twitter-charts",
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)
@app.callback(
    [Output("country-filter", "disabled"),
     Output("topic-search", "disabled")],
    Input("task-type", "value"),
)
def set_options(tasktype):
    topic_disabled, country_disabled = False, False
    if tasktype == 'Trending Topics':
        topic_disabled = True
    if tasktype == 'Average Sentiment':
        country_disabled = True
    return country_disabled, topic_disabled

@app.callback(
    Output("twitter-charts", "children"),
    Input("search", "n_clicks"),
    [
        State("task-type", "value"),
        State("country-filter", "value"),
        State("topic-search", "value")
    ],
)
def updated_charts(n_clicks, tasktype, country, topic):
    if tasktype == 'Trending Topics':
        countryDict = getCountries()
        img = BytesIO()
        wordcloud = getTrendWordcloud(countryDict[country])
        wordcloud.save(img, format='PNG')
        children = [
            html.Div(f'Top Trending Topics in {country} on Twitter', className="photo-title"),
            html.Img(
                src='data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode()),
            ),
        ]
    else:
        percentage = getTweets(topic)
        children = [
            html.Div(f'The topic "{topic}" is {round(percentage, 2)}% positive!', className="photo-title"),
        ]
    return children



