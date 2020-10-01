import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import json


NAV_LOGO = "assets/logo.png"


class NavBar(html.Div):
    """Navbar component"""
    def __init__(self, parent_app):
        super().__init__([])
        self.parent_app = parent_app

        nav_logo = dbc.Row(
            [
                dbc.Col(
                    html.A(
                        html.Img(src=NAV_LOGO, style={"height": "80px"}),
                        href='#',
                        id='navigate-landing-page',
                    ),
                    align="center"
                )
            ],
            justify="center"
        )

        nav_options = dbc.Container([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            children="Data analysis",
                            id='button-data-analysis',
                            className='navbarButton',
                            color='light',
                        ),
                        width={"size": 3},
                        # style={'border-bottom': '1px solid gray'}
                    ),
                    dbc.Col(
                        dbc.Button(
                            children="Train model",
                            id='button-machine-learning',
                            className='navbarButton',
                            color='light',
                        ),
                        width={"size": 3},
                        # style={'border-bottom': '1px solid gray'}
                    ),
                    dbc.Col(
                        dbc.Button(
                            children="About",
                            id='button-about',
                            className='navbarButton',
                            color='light',
                        ),
                        width={"size": 3},
                        # style={'border-bottom': '1px solid gray'}
                    ),
                ],
                justify="center",
            ),
            html.Hr()
        ])

        self.children = dbc.Container(
            [
                nav_logo,
                nav_options
            ],
            style={'width': '60%', "text-align": "center"}
        )

        @self.parent_app.callback(
            [
                Output('button-data-analysis', "className"),
                Output('button-machine-learning', "className"),
                Output('button-about', "className")
            ],
            [
                Input('button-data-analysis', "n_clicks"),
                Input('button-machine-learning', "n_clicks"),
                Input('button-about', "n_clicks")
            ]
        )
        def change_button_css_1(*click):
            ctx = dash.callback_context
            trigger_source = ctx.triggered[0]['prop_id'].split('.')[0]
            if trigger_source == 'button-data-analysis':
                return ['navbarButtonS', 'navbarButton', 'navbarButton']
            elif trigger_source == 'button-machine-learning':
                return ['navbarButton', 'navbarButtonS', 'navbarButton']
            elif trigger_source == 'button-about':
                return ['navbarButton', 'navbarButton', 'navbarButtonS']
            return ['navbarButton', 'navbarButton', 'navbarButton']
