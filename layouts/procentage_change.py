from dash import dcc, html
import plotly.express as px
from fetchdata import df_offer_changes, df_transaction_changes, df_offer_secondary_changes, df_transaction_secondary_changes, df_offer
from darkly_theme import darkly_template
import plotly.io as pio

the_last_quarter = df_offer['kwartal'].iloc[-1]
the_second_to_last_quarter = df_offer['kwartal'].iloc[-2]

pio.templates["darkly"] = darkly_template
pio.templates.default = "darkly"

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


# Add graphs to the layout
percentage_change_layout = html.Div([

    html.H3(f"📊 Zmiany procentowe średniej ceny pomiędzy przedostatnim, {the_second_to_last_quarter}, i ostatnim kwartałem, {the_last_quarter}.",
            style={'textAlign': 'center', 'margin-top': '40px', 'color': '#FFFFFF'}),

    html.Div([
        dcc.Graph(figure=fig_offer_change),
        dcc.Graph(figure=fig_transaction_change),
        dcc.Graph(figure=fig_offer_secondary_change),
        dcc.Graph(figure=fig_transaction_secondary_change),
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'gap': '20px'}),
])




