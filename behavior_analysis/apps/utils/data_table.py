import dash
import dash_table
from dash.dash import no_update
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ALL
import json
import random
import string


class DatatableComponent(html.Div):
    def __init__(self, parent_app, id=None):
        super().__init__([])
        self.parent_app = parent_app
        # Parent defined or randomly generated unique id
        if id is not None:
            self.id = id
        else:
            self.id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))

    def load_data_to_table(self, df):
        self.df = df

        self.table = dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict(),
            style_table={'overflowX': 'auto'},
        )

        self.chidren = [self.table]
