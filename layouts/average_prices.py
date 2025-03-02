from dash import dcc, html, Input, Output
import plotly.express as px
from fetchdata import df_offer, df_transaction, df_offer_secondary, df_transaction_secondary
from app import app
from utils.calculations import get_min_max_kwartal

cities = df_offer.columns[2:].to_list()

df_offer, min_kwartal, max_kwartal = get_min_max_kwartal(df_offer)
df_transaction, min_kwartal, max_kwartal = get_min_max_kwartal(df_transaction)
df_offer_secondary, min_kwartal, max_kwartal = get_min_max_kwartal(df_offer_secondary)
df_transaction_secondary, min_kwartal, max_kwartal = get_min_max_kwartal(df_transaction_secondary)


latest_quarter = df_offer["kwartal_int"].max()
earliest_quarter = latest_quarter - 25

valid_quarters = [year * 10 + q for year in range(2006, 2026) for q in range(1, 5)]

valid_quarters = [q for q in valid_quarters if q <= latest_quarter]

marks = {q: f"Q{q % 10} {q // 10}" for q in valid_quarters if q % 10 == 1}
marks[min(valid_quarters)] = f"Q{min(valid_quarters) % 10} {min(valid_quarters) // 10}"  # Ensure first quarter label
marks[max(valid_quarters)] = f"Q{max(valid_quarters) % 10} {max(valid_quarters) // 10}"  # Ensure last quarter label


prices_layout = html.Div([
    html.H2("🏡 Średnie ceny ofertowe i transakcyjne",
            style={'textAlign': 'center', 'margin-top': '60px', 'color': '#FFFFFF'}),

    # Dropdown (unchanged, keeping dash-bootstrap class)
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
                'backgroundColor': '#333',
                'color': 'white',
                'border': '1px solid #555'
            }
        )
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px'}, className="dash-bootstrap"),

    html.Label("📅 Zaznacz interesujący cię przedział czasowy",
               style={'color': 'white', 'textAlign': 'center', 'display': 'block', 'margin-bottom': '10px',
                      'fontSize': '18px', 'fontWeight': 'bold'}),

    # Styled RangeSlider using custom CSS
    html.Div([
        dcc.RangeSlider(
            id="quarter-rangeslider",
            min=min(valid_quarters),
            max=max(valid_quarters),
            step=None,
            value=[earliest_quarter, latest_quarter],
            marks={k: {'label': v, 'style': {'color': '#ffffff', 'font-size': '12px'}}
                   for k, v in marks.items()},
            tooltip={"placement": "bottom", "always_visible": True},
            updatemode='drag',
            allowCross=False,
            included=True,
            vertical=False,
            className="custom-slider"  # 🔥 Apply custom dark theme styling
        )
    ], style={'width': '85%', 'margin': 'auto', 'padding': '10px'}),

    # Graphs now in a 2x2 layout
    html.Div([
        html.Div([
            dcc.Graph(id='offer-price-chart', style={'width': '48%', 'padding': '10px'}),
            dcc.Graph(id='transaction-price-chart', style={'width': '48%', 'padding': '10px'})
        ], style={'display': 'flex', 'justify-content': 'center', 'gap': '2%'}),

        html.Div([
            dcc.Graph(id='offer-price-secondary-chart', style={'width': '48%', 'padding': '10px'}),
            dcc.Graph(id='transaction-price-secondary-chart', style={'width': '48%', 'padding': '10px'})
        ], style={'display': 'flex', 'justify-content': 'center', 'gap': '2%', 'margin-top': '20px'})
    ])
], style={'backgroundColor': '#2a2a2a', 'padding': '20px', 'borderRadius': '10px'})


@app.callback(
    [Output('offer-price-chart', 'figure'),
     Output('transaction-price-chart', 'figure'),
     Output('offer-price-secondary-chart', 'figure'),
     Output('transaction-price-secondary-chart', 'figure')],
    [Input('cities-dropdown', 'value'),
     Input('quarter-rangeslider', 'value')]  # Added slider input
)
def update_graphs(city, kwartal_range):
    if not city or city not in df_offer.columns:
        return (px.bar(title="Invalid city selected"), px.bar(title="Invalid city selected"),
                px.bar(title="Invalid city selected"), px.bar(title="Invalid city selected"))

    min_kwartal, max_kwartal = kwartal_range

    def filter_df(df):
        return df[(df["kwartal_int"] >= min_kwartal) & (df["kwartal_int"] <= max_kwartal)]

    fig_offer = px.bar(filter_df(df_offer), x="kwartal", y=city, title=f"{city}: Ceny ofertowe - Rynek Pierwotny")
    fig_offer.update_layout(template="darkly")

    fig_transaction = px.bar(filter_df(df_transaction), x="kwartal", y=city,
                             title=f"{city}: Ceny transakcyjne - Rynek Pierwotny")
    fig_transaction.update_layout(template="darkly")

    fig_offer_secondary = px.bar(filter_df(df_offer_secondary), x="kwartal", y=city,
                                 title=f"{city}: Ceny ofertowe - Rynek Wtórny")
    fig_offer_secondary.update_layout(template="darkly")

    fig_transaction_secondary = px.bar(filter_df(df_transaction_secondary), x="kwartal", y=city,
                                       title=f"{city}: Ceny transakcyjne - Rynek Wtórny")
    fig_transaction_secondary.update_layout(template="darkly")

    return fig_offer, fig_transaction, fig_offer_secondary, fig_transaction_secondary