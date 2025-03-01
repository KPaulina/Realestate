import dash
from dash import Dash, dcc, html, Input, Output, callback
import requests
import pandas as pd
import plotly.express as px

from utils.calculations import calculate_percentage_change

# API URLs
API_URL_OFFER = "http://127.0.0.1:8000/ceny_ofertowe"
API_URL_TRANSACTION = "http://127.0.0.1:8000/ceny_transakcyjne"
API_URL_OFFER_SECONDARY = "http://127.0.0.1:8000/ceny_ofertowe_wtorny"
API_URL_TRANSACTION_SECONDARY = "http://127.0.0.1:8000/ceny_transakcyjne_wtorny"


# Fetch data from APIs
def fetch_data(url):
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"❌ Error fetching data from {url}: {e}")
        return pd.DataFrame()


df_offer = fetch_data(API_URL_OFFER)
df_transaction = fetch_data(API_URL_TRANSACTION)
df_offer_secondary = fetch_data(API_URL_OFFER_SECONDARY)
df_transaction_secondary = fetch_data(API_URL_TRANSACTION_SECONDARY)

df_offer_changes = calculate_percentage_change(df_offer)
df_transaction_changes = calculate_percentage_change(df_transaction)
df_offer_secondary_changes = calculate_percentage_change(df_offer_secondary)
df_transaction_secondary_changes = calculate_percentage_change(df_transaction_secondary)

# Extract common city names across all datasets
cities = df_offer.columns[2:].to_list()

# Dash App
app = dash.Dash(__name__)


def generate_percentage_change_graph(df, title):
    """Generate a bar chart showing percentage changes."""
    fig = px.bar(df, x="cities", y="price_percentage_change", title=title, labels={"price_percentage_change": "Zmiana %"})
    fig.update_layout(xaxis_tickangle=-45)
    return dcc.Graph(figure=fig)


app.layout = html.Div([
    html.H1("Polska ceny nieruchomości", style={'textAlign': 'center', 'margin-bottom': '20px'}),

    html.Div([
        dcc.Dropdown(
            options=[{'label': city, 'value': city} for city in cities],
            value=cities[14] if len(cities) > 0 else None,
            id='cities-dropdown',
            clearable=False,
            searchable=True,
            style={'width': '40%', 'margin': 'auto', 'font-size': '16px'}
        )
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '30px'}),

    # 🔹 Najpierw wykresy zmian procentowych
    html.H2("Zmiany procentowe cen", style={'textAlign': 'center', 'margin-top': '40px'}),

    html.Div([
        dcc.Graph(id='offer-change-chart'),
        dcc.Graph(id='transaction-change-chart'),
        dcc.Graph(id='offer-secondary-change-chart'),
        dcc.Graph(id='transaction-secondary-change-chart'),
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'gap': '20px'}),

    # 🔹 Dopiero potem wykresy średnich cen
    html.H2("Średnie ceny ofertowe i transakcyjne", style={'textAlign': 'center', 'margin-top': '40px'}),

    html.Div([
        dcc.Graph(id='offer-price-chart', figure=px.bar(title="Ceny ofertowe - Rynek Pierwotny")),
        dcc.Graph(id='transaction-price-chart', figure=px.bar(title="Ceny transakcyjne - Rynek Pierwotny")),
        dcc.Graph(id='offer-price-secondary-chart', figure=px.bar(title="Ceny ofertowe - Rynek Wtórny")),
        dcc.Graph(id='transaction-price-secondary-chart', figure=px.bar(title="Ceny transakcyjne - Rynek Wtórny"))
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'gap': '20px'}),
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


@app.callback(
    [Output('offer-change-chart', 'figure'),
     Output('transaction-change-chart', 'figure'),
     Output('offer-secondary-change-chart', 'figure'),
     Output('transaction-secondary-change-chart', 'figure')],
    Input('cities-dropdown', 'value')
)
def update_percentage_change_graph(_):
    fig_offer = px.bar(df_offer_changes, x="cities", y="price_percentage_change",
                       title="Zmiana procentowa - Ceny Ofertowe (Rynek Pierwotny)",
                       color="price_percentage_change",
                       color_continuous_scale="RdYlGn")

    fig_transaction = px.bar(df_transaction_changes, x="cities", y="price_percentage_change",
                             title="Zmiana procentowa - Ceny Transakcyjne (Rynek Pierwotny)",
                             color="price_percentage_change",
                             color_continuous_scale="RdYlGn")

    fig_offer_secondary = px.bar(df_offer_secondary_changes, x="cities", y="price_percentage_change",
                                 title="Zmiana procentowa - Ceny Ofertowe (Rynek Wtórny)",
                                 color="price_percentage_change",
                                 color_continuous_scale="RdYlGn")

    fig_transaction_secondary = px.bar(df_transaction_secondary_changes, x="cities", y="price_percentage_change",
                                       title="Zmiana procentowa - Ceny Transakcyjne (Rynek Wtórny)",
                                       color="price_percentage_change",
                                       color_continuous_scale="RdYlGn")

    return fig_offer, fig_transaction, fig_offer_secondary, fig_transaction_secondary


if __name__ == "__main__":
    app.run_server(debug=True)
