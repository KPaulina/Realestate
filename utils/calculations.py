import pandas as pd


def calculate_percentage_change(df: pd.DataFrame) -> pd.DataFrame:
    cities = ['bialystok', 'bydgoszcz', 'gdansk', 'gdynia', 'katowice', 'kielce', 'krakow', 'lublin', 'lodz', 'olsztyn',
              'opole', 'poznan', 'rzeszow', 'szczecin', 'warszawa', 'wroclaw', 'zielona_gora']
    changes_offer = {}
    for city in cities:
        changes_offer[city] = ((df[city].iloc[-1] - df[city].iloc[-2]) / df[city].iloc[-2]) * 100
    df = pd.DataFrame.from_dict(changes_offer, orient='index', columns=['price_percentage_change'])
    df = df.sort_values(by=['price_percentage_change'])
    df['cities'] = df.index
    return df


def kwartal_to_int(kwartal):
    kwartal_order = {"I": 1, "II": 2, "III": 3, "IV": 4, "VI": 4}  # Fix 'VI' as 'IV'

    try:
        quarter, year = kwartal.split()
        quarter = kwartal_order.get(quarter, None)  # Get valid quarter or None
        if quarter is None:
            raise ValueError(f"Invalid quarter: {quarter}")
        return int(f"{year}{quarter}")  # Converts to YYYYQ format (e.g., 20241)
    except ValueError as e:
        print(f"Error converting '{kwartal}' to int: {e}")
        return None  # Return None for invalid entries


def get_min_max_kwartal(df, column_name="kwartal"):
    df = df.copy()  # Avoid modifying the original DataFrame
    df["kwartal_int"] = df[column_name].apply(kwartal_to_int)  # Convert column to int
    df.dropna(subset=["kwartal_int"], inplace=True)  # Remove invalid rows

    if df.empty:
        return df, None, None  # Handle case where all values were invalid

    min_kwartal = int(df["kwartal_int"].min())  # 🔥 Convert to Python int
    max_kwartal = int(df["kwartal_int"].max())  # 🔥 Convert to Python int

    return df, min_kwartal, max_kwartal

# Example DataFrame
