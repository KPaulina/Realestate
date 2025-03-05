from dash import html, Input, Output
import dash_bootstrap_components as dbc

from app import app
from layouts.average_prices import prices_layout
from layouts.procentage_change import percentage_change_layout
from layouts.biggest_diff_offer_trans import diff_layout
from darkly_theme import darkly_template
import plotly.io as pio

pio.templates["darkly"] = darkly_template
pio.templates.default = "darkly"

app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Średnie ceny", tab_id="tab-prices",
                        labelClassName="text-light fw-bold bg-dark rounded-top",
                        activeLabelClassName="text-white fw-bold bg-success"),
                dbc.Tab(label="Analiza procentowa kw/kw",
                        tab_id="tab-trends",
                        labelClassName="text-light fw-bold bg-dark rounded-top",
                        activeLabelClassName="text-white fw-bold bg-danger"
                        ),
                dbc.Tab(label="Różnica cen",
                        tab_id="tab-diff",
                        labelClassName="text-light fw-bold bg-dark rounded-top",
                        activeLabelClassName="text-white fw-bold bg-danger"
                        ),
                            ],
            id="tabs",
            active_tab="tab-prices",
            className="mb-3 border-bottom",
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
    elif tab_chosen == "tab-diff":
        return diff_layout
    return html.P("This shouldn't be displayed for now...")


if __name__=='__main__':
    app.run_server(debug=True)