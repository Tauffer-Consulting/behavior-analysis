from ..models import Experiment, Group, Subject
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.dash import no_update
from .utils.data_table import DatatableComponent
from .utils.graph_tsne import GraphTsne
from .utils.table_subjects import SubjectsTable
from pandas_profiling import ProfileReport
import pandas as pd
import json
import base64
import random
import string
import io


class PageSimplevis(html.Div):
    def __init__(self, parent_app, id=None):
        super().__init__([])
        self.parent_app = parent_app
        # Parent defined or randomly generated unique id
        if id is not None:
            self.id = id
        else:
            self.id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))

        self.button_load_data = dcc.Upload(
            id='button-load-data',
            children=dbc.Button("Load data", color='dark')
        )

        self.profile_summary = html.Iframe(
            # src='static/output.html',
            id="iframe-profile-summary",
            style={"border": 0, "width": "100%", "height": "900px", "overflow": "auto"}
        )

        # Tabs
        subjects = Subject.query.all()
        for s in subjects:
            subjects_table = SubjectsTable(parent_app=parent_app, subjects=subjects)

        tab1_content = dbc.Card(
            dbc.CardBody(
                id='tab1',
                children=[dbc.Row([
                    dbc.Col(
                        [
                            dcc.Loading(
                                id="loading-tab1",
                                type="circle",
                                color='#343a40',
                                children=html.Div(children=[subjects_table], id="tab1-data-table")
                            ),
                        ],
                    )
                ], justify="center")],
            ),
        )

        @self.parent_app.callback(
            [
                Output('tab1-data-table', 'children'),
                Output('iframe-profile-summary', 'src'),
            ],
            [Input('button-load-data', 'contents')],
        )
        def update_output(content):
            if content is not None:
                # Read and decode content
                content_type, content_string = content.split(',')
                decoded = base64.b64decode(content_string)
                self.df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), index_col=0)

                # Make data table for tab 1
                table = dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i, "hideable": True, "renamable": True} for i in self.df.columns],
                    data=self.df.head(100).to_dict('records'),
                    style_table={
                        'overflowX': 'auto', 'height': '300px', 'overflowY': 'auto',
                    },
                    style_cell={
                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                    },
                )

                # Make profile summary for tab 2
                # profile = df.profile_report(title="")
                # profile.to_file("static/output.html")

                return [table, 'static/output.html']
            return [no_update, no_update]

        tab2_content = dbc.Card(
            dbc.CardBody(
                id='tab2',
                children=[
                    dbc.Row([
                        dbc.Col(
                            [
                                html.Div(
                                    children=[self.profile_summary],
                                    id="tab2-profile-summary",
                                )
                            ],
                        )
                    ], justify="center")
                ]
            ),
        )

        tab3_content = dbc.Card(
            dbc.CardBody(
                id='tab3',
                children=[
                    dbc.Button("Run t-SNE", color='dark', id='button-run-tsne'),
                    html.Br(),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(
                            [
                                dcc.Loading(
                                    id="loading-tab3",
                                    type="circle",
                                    color='#343a40',
                                    children=html.Div(children=[], id="tab3-graph_tsne")
                                ),
                            ],
                        )
                    ], justify="center")
                ]
            ),
        )

        @self.parent_app.callback(
            Output("tab3-graph_tsne", "children"),
            [Input('button-run-tsne', "n_clicks")]
        )
        def function_run_tsne(n_clicks):
            if n_clicks is not None:
                self.tsne_vis = GraphTsne(parent_app=parent_app, df=self.df, id='simple-vis-tsne')
                return [self.tsne_vis]
            return no_update

        # Tabs layout
        tabs = dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Data table"),
                dbc.Tab(tab2_content, label="Summary"),
                dbc.Tab(tab3_content, label="t-SNE"),
            ]
        )

        # Children - main layout
        self.children = dbc.Container([
            self.button_load_data,
            html.Br(),
            tabs,
            html.Br(),
            html.Br()
        ])

        # @self.parent_app.callback(
        #     Output("graphs-page-content", "children"),
        #     [
        #         Input("graphs-timeline-link", "n_clicks"),
        #         Input("graphs-distribution-link", "n_clicks"),
        #         Input("graphs-map-link", "n_clicks"),
        #     ]
        # )
        # def render_graphs_page_content(*c1):
        #     ctx = dash.callback_context
        #     trigger_source = ctx.triggered[0]['prop_id'].split('.')[0]
        #     if trigger_source == 'graphs-timeline-link':
        #         return self.graph_timeline
        #     elif trigger_source == 'graphs-timeline-lin':
        #         return html.P("Another graph to be produced")
        #     elif trigger_source == 'graphs-timeline-lin':
        #         return html.P("a map")
        #     return self.graph_timeline
