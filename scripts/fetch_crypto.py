import requests
import pandas as pd
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# -----------------------------
# 📡 EXTRACTION
# -----------------------------
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        return []


# -----------------------------
# 🔄 TRANSFORMATION
# -----------------------------
def transform_data(data):
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    df = df[[
        'name',
        'current_price',
        'market_cap',
        'total_volume',
        'price_change_percentage_24h'
    ]]

    # Ajout timestamp
    df['timestamp'] = datetime.now()

    return df


# -----------------------------
# 🗄️ LOAD (POSTGRES)
# -----------------------------
def save_to_postgres(df):
    if df.empty:
        print("⚠️ Aucune donnée à insérer")
        return

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", 5432)
        )
        cur = conn.cursor()

        # Création table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id SERIAL PRIMARY KEY,
                name TEXT,
                current_price FLOAT,
                market_cap BIGINT,
                total_volume BIGINT,
                price_change_percentage_24h FLOAT,
                timestamp TIMESTAMP
            )
        ''')

        # Batch insert (rapide 🔥)
        records = [
            (
                row['name'],
                row['current_price'],
                row['market_cap'],
                row['total_volume'],
                row['price_change_percentage_24h'],
                row['timestamp']
            )
            for _, row in df.iterrows()
        ]

        cur.executemany('''
            INSERT INTO crypto_prices (
                name,
                current_price,
                market_cap,
                total_volume,
                price_change_percentage_24h,
                timestamp
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', records)

        conn.commit()
        cur.close()
        conn.close()

        print(f"✅ {len(records)} lignes insérées dans PostgreSQL")

    except Exception as e:
        print(f"❌ Erreur PostgreSQL: {e}")


# -----------------------------
# 🚀 MAIN PIPELINE
# -----------------------------
def main():
    print("🚀 Lancement du pipeline crypto...")

    data = fetch_crypto_data()
    df = transform_data(data)

    save_to_postgres(df)

    print("🎉 Pipeline terminé.")


if __name__ == "__main__":
    main()