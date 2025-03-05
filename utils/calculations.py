import pandas as pd
from typing import List, Tuple, Optional

CITIES = ['bialystok', 'bydgoszcz', 'gdansk', 'gdynia', 'katowice', 'kielce', 'krakow',
          'lublin', 'lodz', 'olsztyn', 'opole', 'poznan', 'rzeszow', 'szczecin',
          'warszawa', 'wroclaw', 'zielona_gora']


def calculate_percentage_change(df: pd.DataFrame) -> pd.DataFrame:
    changes_offer = {}
    for city in CITIES:
        changes_offer[city] = ((df[city].iloc[-1] - df[city].iloc[-2]) / df[city].iloc[-2]) * 100
    df = pd.DataFrame.from_dict(changes_offer, orient='index', columns=['price_percentage_change'])
    df = df.sort_values(by=['price_percentage_change'])
    df['cities'] = df.index
    return df


def kwartal_to_int(kwartal) -> Optional[int]:
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


def get_min_max_kwartal(df, column_name="kwartal") -> Tuple[pd.DataFrame, Optional[int], Optional[int]]:
    df = df.copy()  # Avoid modifying the original DataFrame
    df["kwartal_int"] = df[column_name].apply(kwartal_to_int)  # Convert column to int
    df.dropna(subset=["kwartal_int"], inplace=True)  # Remove invalid rows

    if df.empty:
        return df, None, None  # Handle case where all values were invalid

    min_kwartal = int(df["kwartal_int"].min())  # 🔥 Convert to Python int
    max_kwartal = int(df["kwartal_int"].max())  # 🔥 Convert to Python int

    return df, min_kwartal, max_kwartal


def get_quarter_calculations(df: pd.DataFrame) -> tuple[int, int, List[int]]:
    latest_quarter = df["kwartal_int"].max()

    valid_quarters = [year * 10 + q for year in range(2006, 2026) for q in range(1, 5)]

    valid_quarters = [q for q in valid_quarters if q <= latest_quarter]
    earliest_quarter = valid_quarters[-10]
    return latest_quarter, earliest_quarter, valid_quarters


def calculate_biggest_price_change(df_offer: pd.DataFrame, df_transaction: pd.DataFrame) -> pd.DataFrame:
    df_offer.iloc[:, 2:] = df_offer.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')
    df_transaction.iloc[:, 2:] = df_transaction.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')
    # null values will be a problem, so they are replaced with 0
    df_offer.iloc[:, 2:].fillna(0, inplace=True)
    df_transaction.iloc[:, 2:].fillna(0, inplace=True)

    df_price_diff = df_offer.copy()
    df_price_diff.iloc[:, 2:] = df_offer.iloc[:, 2:] - df_transaction.iloc[:, 2:]

    last_quarter = df_price_diff["kwartal"].max()
    # the last quarter
    df_last_quarter = df_price_diff[df_price_diff["kwartal"] == last_quarter]

    # Drop non-city columns ('id' and 'kwartal') to focus only on price differences
    df_last_quarter_values = df_last_quarter.iloc[:, 2:]
    df_top_gaps = df_last_quarter_values.abs().mean().sort_values(ascending=False)
    df_top_gaps = df_top_gaps.reset_index()  # Convert Series to DataFrame
    df_top_gaps.columns = ["Miasto", "Cena"]  # Rename columns
    return df_top_gaps[df_top_gaps["Miasto"].isin(CITIES)]


def calculate_relative_price_gap(df_offer: pd.DataFrame, df_transaction: pd.DataFrame) -> pd.DataFrame:
    # Ensure only numeric columns (excluding 'id' and 'kwartal') are converted, handling errors
    df_offer.iloc[:, 2:] = df_offer.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')
    df_transaction.iloc[:, 2:] = df_transaction.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')

    # Align both DataFrames to ensure they have the same structure
    df_transaction = df_transaction.reindex(df_offer.index)
    df_transaction = df_transaction[df_offer.columns]

    # Fill missing values with 0 or interpolate them (choose one strategy)
    df_offer.iloc[:, 2:].fillna(0, inplace=True)  # or df_offer.iloc[:, 2:].interpolate(inplace=True)
    df_transaction.iloc[:, 2:].fillna(0, inplace=True)

    # Compute absolute price difference (excluding first two columns)
    df_price_diff = df_offer.copy()
    df_price_diff.iloc[:, 2:] = df_offer.iloc[:, 2:] - df_transaction.iloc[:, 2:]

    # Compute relative difference (percentage difference)
    df_relative_diff = df_price_diff.copy()
    df_relative_diff.iloc[:, 2:] = (df_price_diff.iloc[:, 2:] / df_offer.iloc[:, 2:]) * 100

    # Replace any NaN values resulting from division by zero
    df_relative_diff.fillna(0, inplace=True)

    # Select the last available quarter
    last_quarter = df_price_diff["kwartal"].max()

    # Filter data for the last quarter
    df_last_quarter = df_price_diff[df_price_diff["kwartal"] == last_quarter]

    # Drop non-city columns ('id' and 'kwartal') to focus only on price differences
    df_last_quarter_values = df_last_quarter.iloc[:, 2:]

    # Absolute price difference
    df_top_gaps = df_last_quarter_values.abs().mean().sort_values(ascending=False)

    # Calculate relative difference (percentage gap)
    df_relative_gap = (df_last_quarter_values / df_offer[df_offer["kwartal"] == last_quarter].iloc[:, 2:]).abs() * 100

    # Sort by largest relative gap
    df_relative_gap_sorted = df_relative_gap.mean().sort_values(ascending=False)

    df_relative_gap_sorted = df_relative_gap_sorted.reset_index()  # Convert Series to DataFrame
    df_relative_gap_sorted.columns = ["Miasto", "Procent"]  # Rename columns
    return df_relative_gap_sorted[df_relative_gap_sorted["Miasto"].isin(CITIES)]
