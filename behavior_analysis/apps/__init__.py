import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from .main_page import MainPage


def init_app_home(server):
    FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
    local_css = '/assets/style.css'
    external_stylesheets = [dbc.themes.BOOTSTRAP, FONT_AWESOME, local_css]
    dash_app = dash.Dash(
        server=server,
        external_stylesheets=external_stylesheets,
        suppress_callback_exceptions=True,
        routes_pathname_prefix='/',
        title='Behavior analysis'
    )

    # Create Dash Layout
    dash_app.layout = html.Div([
        MainPage(parent_app=dash_app)
    ])
    dash_app.enable_dev_tools(debug=True)

    return dash_app.server
