import requests
import pandas as pd
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

cities = df_offer.columns[2:].to_list()

df_offer_changes = calculate_percentage_change(df_offer)
df_transaction_changes = calculate_percentage_change(df_transaction)
df_offer_secondary_changes = calculate_percentage_change(df_offer_secondary)
df_transaction_secondary_changes = calculate_percentage_change(df_transaction_secondary)