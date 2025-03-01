import dash
from dash import Dash, dcc, html, Input, Output, callback
import requests
import pandas as pd
import plotly.express as px
from fetchdata import df_offer, df_transaction, df_offer_secondary, df_transaction_secondary
from app import app

cities = df_offer.columns[2:].to_list()

prices_layout = html.Div([
    html.H2("🏡 Średnie ceny ofertowe i transakcyjne",
                style={'textAlign': 'center', 'margin-top': '60px', 'color': '#444'}),

    # Dropdown dla wyboru miasta (przeniesiony tutaj)
    html.Div([

        dcc.Dropdown(
            id='cities-dropdown',
            options=[{'label': city, 'value': city} for city in cities],
            value=cities[14] if len(cities) > 0 else None,
            clearable=False,
            searchable=True,
            style={
                'width': '40%',
                'margin': '10px auto',
                'font-size': '14px',
                'padding': '5px',
                'border-radius': '5px',
                'background-color': 'white'
            }
        )
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '30px'}),

    html.Div([
        dcc.Graph(id='offer-price-chart', style={'padding': '10px'}),
        dcc.Graph(id='transaction-price-chart', style={'padding': '10px'}),
        dcc.Graph(id='offer-price-secondary-chart', style={'padding': '10px'}),
        dcc.Graph(id='transaction-price-secondary-chart', style={'padding': '10px'})
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'gap': '20px'}),
])


@app.callback(
    [Output('offer-price-chart', 'figure'),
     Output('transaction-price-chart', 'figure'),
     Output('offer-price-secondary-chart', 'figure'),
     Output('transaction-price-secondary-chart', 'figure')],
    Input('cities-dropdown', 'value')
)
def update_graphs(city):
    if not city or city not in df_offer.columns:
        return (px.bar(title="Invalid city selected"), px.bar(title="Invalid city selected"),
                px.bar(title="Invalid city selected"), px.bar(title="Invalid city selected"))

    fig_offer = px.bar(df_offer, x="kwartal", y=city, title=f"{city}: Ceny ofertowe - Rynek Pierwotny")
    fig_transaction = px.bar(df_transaction, x="kwartal", y=city, title=f"{city}: Ceny transakcyjne - Rynek Pierwotny")
    fig_offer_secondary = px.bar(df_offer_secondary, x="kwartal", y=city, title=f"{city}: Ceny ofertowe - Rynek Wtórny")
    fig_transaction_secondary = px.bar(df_transaction_secondary, x="kwartal", y=city,
                                       title=f"{city}: Ceny transakcyjne - Rynek Wtórny")

    return fig_offer, fig_transaction, fig_offer_secondary, fig_transaction_secondary