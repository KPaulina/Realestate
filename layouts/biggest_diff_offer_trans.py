from dash import dcc, html, Input, Output
import plotly.express as px
from fetchdata import df_offer, df_transaction, df_offer_secondary, df_transaction_secondary
from app import app
from utils.calculations import calculate_biggest_price_change

df_absolute_gap, df_relative_gap  = calculate_biggest_price_change(df_offer, df_transaction)
df_absolute_gap_secondary, df_relative_gap_secondary = calculate_biggest_price_change(df_offer_secondary,
                                                                                      df_transaction_secondary)

diff_layout = html.Div([
    html.H3("📊 Analiza różnic między cenami ofertowymi i transakcyjnymi", style={'textAlign': 'center'}),

    # Absolute gap charts
    dcc.Graph(id="absolute-gap-chart"),
    dcc.Graph(id="absolute-gap-chart_secondary"),

    html.H3("📉 Miasta z największą względną różnicą cen", style={'textAlign': 'center', 'margin-top': '40px'}),

    # Relative gap charts
    dcc.Graph(id="relative-gap-chart"),
    dcc.Graph(id="relative-gap-chart_secondary"),

    # Dummy inputs to trigger updates
    dcc.Interval(id="dummy-absolute", interval=1000, n_intervals=0),
    dcc.Interval(id="dummy-relative", interval=1000, n_intervals=0)
])


@app.callback(
    [Output("absolute-gap-chart", "figure"),
     Output("absolute-gap-chart_secondary", "figure")],
    Input("absolute-gap-chart", "id")  # Dummy input to trigger update once
)
def update_price_gap_graphs(_):
    # Absolute gap chart
    fig_absolute = px.bar(df_absolute_gap, x="Miasto", y="Cena",
                          title="🔹 Miasta z największą absolutną różnicą cen na rynku pierwotnym",
                          labels={"Cena": "Różnica w zł"},
                          color="Cena",
                          color_continuous_scale="Blues")

    # Relative gap chart
    fig_absolute_sec = px.bar(df_absolute_gap_secondary, x="Miasto", y="Cena",
                           title="🔹 Miasta z największą absolutną różnicą cen na rynku wtórnym",
                           labels={"Cena": "Różnica w zł"},
                           color="Cena",
                           color_continuous_scale="Reds")

    return fig_absolute, fig_absolute_sec


@app.callback(
    [Output("relative-gap-chart", "figure"),
     Output("relative-gap-chart_secondary", "figure")],
    Input("dummy-relative", "n_intervals")  # Triggers updates
)
def update_relative_gap_graphs(_):
    # Relative gap - Primary Market
    fig_relative = px.bar(df_relative_gap, x="Miasto", y="Procent",
                          title="🔹 Miasta z największą względną różnicą cen na rynku pierwotnym",
                          labels={"Procent": "Różnica %"},
                          color="Procent",
                          color_continuous_scale="Greens")

    # Relative gap - Secondary Market
    fig_relative_sec = px.bar(df_relative_gap_secondary, x="Miasto", y="Procent",
                              title="🔹 Miasta z największą względną różnicą cen na rynku wtórnym",
                              labels={"Procent": "Różnica %"},
                              color="Procent",
                              color_continuous_scale="Oranges")

    return fig_relative, fig_relative_sec
