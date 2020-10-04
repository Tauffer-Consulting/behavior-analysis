from ...models import Experiment, Group, Subject
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from dash.dash import no_update
import random
import string


class SubjectsTable(dbc.Table):
    def __init__(self, parent_app, subjects, id=None):
        super().__init__()
        self.parent_app = parent_app
        # User chosen or randomly generated unique id
        if id is None:
            self.id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
        else:
            self.id = id

        self.bordered = False
        self.hover = True
        self.responsive = True
        self.striped = False

        table_header = html.Thead(html.Tr([
            html.Th(dbc.Checkbox(id='check-subject-all')),
            html.Th("ID"),
            html.Th("Experiment"),
            html.Th("Group"),
            html.Th("Date")
        ]))

        table_body = html.Tbody([])
        for sub in subjects:
            group = sub.group
            # Group.query.filter_by(name=s['group']).first()
            row = html.Tr([
                html.Td(dbc.Checkbox(id={'type': 'check-subject', 'index': sub.id})),
                html.Td(sub.id),
                html.Td(group.experiment.name),
                html.Td(group.name),
                html.Td(str(sub.date.date()))
            ])
            table_body.children.append(row)

        # @self.parent_app.callback(
        #     Output({'type': 'check-subject', 'index': 2}, 'checked'),
        #     [Input('check-subject-all', 'checked')],
        # )
        # def toggle_check_all(chk):
        #     return no_update

        self.children = [
            table_header,
            table_body
        ]
