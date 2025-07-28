from datetime import datetime

import psycopg2
import requests
from psycopg2.extras import execute_values

# Database config (update as needed)
DB_CONFIG = {
    "dbname": "crypto_db",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": "5432",
}


# Connect to PostgreSQL
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# Fetch coins list from CoinGecko
def fetch_coins():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# Fetch market data for top N coins by market cap
def fetch_market_data(vs_currency="usd", per_page=50, page=1):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "price_change_percentage": "24h",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


# Insert coins into DB
def insert_coins(coins):
    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO coins (id, symbol, name)
                VALUES %s
                ON CONFLICT (id) DO NOTHING
            """,
                [(c["id"], c["symbol"], c["name"]) for c in coins],
            )


# Insert market data


def insert_market_data(market_data):
    with get_connection() as conn:
        with conn.cursor() as cur:
            records = []
            for c in market_data:
                records.append(
                    (
                        c["id"],
                        c.get("current_price"),
                        c.get("market_cap"),
                        c.get("market_cap_rank"),
                        c.get("total_volume"),
                        c.get("high_24h"),
                        c.get("low_24h"),
                        c.get("price_change_24h"),
                        c.get("price_change_percentage_24h"),
                        c.get("circulating_supply"),
                        c.get("total_supply"),
                        c.get("max_supply"),
                        datetime.fromisoformat(
                            c["last_updated"].replace("Z", "+00:00")
                        ),
                    )
                )
            execute_values(
                cur,
                """
                INSERT INTO coin_market_data (
                    coin_id, current_price, market_cap, market_cap_rank,
                    total_volume, high_24h, low_24h,
                    price_change_24h, price_change_percentage_24h,
                    circulating_supply, total_supply, max_supply,
                    last_updated
                ) VALUES %s
                ON CONFLICT (coin_id, last_updated) DO NOTHING
            """,
                records,
            )


if __name__ == "__main__":
    print("Fetching coin list...")
    coins = fetch_coins()
    insert_coins(coins)
    print(f"Inserted {len(coins)} coins.")

    print("Fetching market data...")
    market_data = fetch_market_data(per_page=50)
    insert_market_data(market_data)
    print(f"Inserted market data for {len(market_data)} coins.")
