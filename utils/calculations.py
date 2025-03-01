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