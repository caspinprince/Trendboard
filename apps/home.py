import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div(
    dbc.Container([
        html.Div(
            children = [
                html.H1("Welcome to Trendboard", className="header-title-2")
            ]
        ),
        html.Div(
            children = [
                html.P(
                    children='Trendboard is a dashboard that analyzes trends in the latest data from social media APIs!',
                    className='main-description',
                )

            ]
        ),
        html.Div(
            children = [
                html.P(
                    children='The dashboard is split into two sections: one for Youtube Data, one for Twitter Data.',
                    className='main-description',
                )

            ]
        ),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    children=[
                        html.H3(children='Access the code and a detailed description for this dashboard', className="info-card"),
                        dbc.Button(
                            "GitHub",
                            href="https://github.com/caspinprince/Trendboard",
                            color="primary",
                            className="mt-3"
                        ),
                    ],
                    body=True,
                    color="dark",
                    outline=True
                ),
                width=7,
                className="mb-4"
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        html.H3(children='Learn more about the APIs and model used in this dashboard', className="info-card"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Button(
                                    "Youtube API",
                                    href="https://developers.google.com/youtube/v3",
                                    color="primary",
                                ),
                                className="mt-3"
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Twitter API",
                                    href="https://developer.twitter.com/en/docs/twitter-api/v1",
                                    color="primary",
                                ),
                                className="mt-3"
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "ML Model",
                                    href="https://github.com/caspinprince/Trendboard/blob/main/assets/twitter_sentiment_analysis_model.ipynb",
                                    color="primary",
                                ),
                                className="mt-3"
                            )
                        ],
                        justify="center"
                        )
                    ],
                    body=True,
                    color="dark",
                    outline=True
                ),
                width=7, className="mb-4"
            ),
        ],
        className="main-page"
        ),
    ])
)
