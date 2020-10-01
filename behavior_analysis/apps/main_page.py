import dash
from dash.dash import no_update
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ALL
from .utils.navbar import NavBar
from .page_simple_vis import PageSimplevis

import json


class MainPage(html.Div):
    def __init__(self, parent_app):
        super().__init__([])
        self.parent_app = parent_app

        # Navbar
        self.navbar = NavBar(parent_app=parent_app)

        # Landing page
        self.landing_page = PageSimplevis(parent_app=parent_app)

        # Quote entry page
        self.simple_vis = []  # PageSimplevis(parent_app=parent_app)

        self.children = html.Div([
            self.navbar,
            html.Div([], id='main-page-content')
        ])

        @self.parent_app.callback(
            Output('main-page-content', "children"),
            [
                Input('button-data-analysis', "n_clicks"),
                Input('button-machine-learning', "n_clicks"),
                Input('button-about', "n_clicks")
            ]
        )
        def change_page_content(*click):
            ctx = dash.callback_context
            trigger_source = ctx.triggered[0]['prop_id'].split('.')[0]
            if trigger_source == 'button-data-analysis':
                return self.landing_page
            elif trigger_source == 'button-machine-learning':
                return no_update
            elif trigger_source == 'button-about':
                return []
            return self.landing_page #no_update
