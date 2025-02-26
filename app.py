import dash
from dash import dcc, html
import requests
import pandas as pd
import plotly.express as px

# Define API URL and table name
API_URL = "http://127.0.0.1:8000/ceny_ofertowe"  # Change this to the correct table name

# Fetch data from FastAPI
try:
    response = requests.get(API_URL)
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Ensure required columns exist
    if "kwartal" in df.columns and "warszawa" in df.columns:
        # Create Bar Chart for Warsaw
        fig = px.bar(df, x="kwartal", y="warszawa", title="Price Changes in Warsaw")
    else:
        raise ValueError("Missing required columns in API response")

except Exception as e:
    print("❌ Error fetching data:", e)
    df = pd.DataFrame()
    fig = px.bar(title="Error loading data")

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Warsaw Property Prices"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)

