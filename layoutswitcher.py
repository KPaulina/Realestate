import dash
from dash import Dash, dcc, html, Input, Output, callback
import requests
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

from app import app
from layouts.average_prices import prices_layout
from layouts.procentage_change import percentage_change_layout


app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Średnie ceny", tab_id="tab-prices", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Analiza procentowa", tab_id="tab-trends", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                # dbc.Tab(label="Other", tab_id="tab-other", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="tab-prices",
        ),
    ], className="mt-3"
)

app.layout = dbc.Container([
    html.H1("Polska ceny nieruchomości", style={'textAlign': 'center', 'margin-bottom': '20px'}),
    html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
    html.Div(id='content', children=[])

])


@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-prices":
        return prices_layout
    elif tab_chosen == "tab-trends":
        return percentage_change_layout
    return html.P("This shouldn't be displayed for now...")


if __name__=='__main__':
    app.run_server(debug=True)