import dash
import dash_bootstrap_components as dbc


# Dash App
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )