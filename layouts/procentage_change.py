from dash import dcc, html
import plotly.express as px
from fetchdata import df_offer_changes, df_transaction_changes, df_offer_secondary_changes, df_transaction_secondary_changes

fig_offer_change = px.bar(df_offer_changes, x="cities", y="price_percentage_change",
                          title="Zmiana procentowa - Ceny Ofertowe (Rynek Pierwotny)",
                          color="price_percentage_change",
                          labels={"price_percentage_change": "Zmiany procentowe", "cities": "Miasta"},
                          color_continuous_scale="RdYlGn")

fig_transaction_change = px.bar(df_transaction_changes, x="cities", y="price_percentage_change",
                                title="Zmiana procentowa - Ceny Transakcyjne (Rynek Pierwotny)",
                                color="price_percentage_change",
                                labels={"price_percentage_change": "Zmiany procentowe", "cities": "Miasta"},
                                color_continuous_scale="RdYlGn")

fig_offer_secondary_change = px.bar(df_offer_secondary_changes, x="cities", y="price_percentage_change",
                                    title="Zmiana procentowa - Ceny Ofertowe (Rynek Wtórny)",
                                    color="price_percentage_change",
                                    labels={"price_percentage_change": "Zmiany procentowe", "cities": "Miasta"},
                                    color_continuous_scale="RdYlGn")

fig_transaction_secondary_change = px.bar(df_transaction_secondary_changes, x="cities", y="price_percentage_change",
                                          title="Zmiana procentowa - Ceny Transakcyjne (Rynek Wtórny)",
                                          color="price_percentage_change",
                                          labels={"price_percentage_change": "Zmiany procentowe", "cities": "Miasta"},
                                          color_continuous_scale="RdYlGn")

# Add graphs directly to the layout
percentage_change_layout = html.Div([

    html.H2("📊 Zmiany procentowe średniej ceny pomiędzy przedostatnim i ostatnim kwartałem",
            style={'textAlign': 'center', 'margin-top': '40px', 'color': '#444'}),

    html.Div([
        dcc.Graph(figure=fig_offer_change),
        dcc.Graph(figure=fig_transaction_change),
        dcc.Graph(figure=fig_offer_secondary_change),
        dcc.Graph(figure=fig_transaction_secondary_change),
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'gap': '20px'}),
])




