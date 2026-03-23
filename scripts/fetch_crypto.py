import requests
import pandas as pd
import sqlite3
from datetime import datetime
import os

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def transform_data(data):
    df = pd.DataFrame(data)
    df = df[['name', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h']]
    df['timestamp'] = datetime.now()
    return df

def save_to_db(df, db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql("crypto_prices", conn, if_exists="append", index=False)
    conn.close()

def main():
    data = fetch_crypto_data()
    df = transform_data(data)
    db_path = os.path.join(os.path.dirname(__file__), '../database/crypto.db')
    save_to_db(df, db_path)
    print("Données sauvegardées dans la base de données.")

if __name__ == "__main__":
    main()
