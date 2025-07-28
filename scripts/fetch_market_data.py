import logging
import os
from datetime import datetime

import psycopg2
import requests
from dotenv import load_dotenv
from psycopg2.extras import execute_values

# Load .env variables
load_dotenv()

# Logging config
LOG_FILE = os.path.join(
    os.path.dirname(__file__), "..", "logs", "fetch_market_data.log"
)
logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

# Database config
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
}


# PostgreSQL connection
def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        logging.error("DB connection failed: %s", e)
        raise


# Fetch top N coins market data
def fetch_market_data(vs_currency="usd", per_page=50, page=1):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "price_change_percentage": "24h",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logging.info("Fetched market data for %d coins", len(data))
        return data
    except Exception as e:
        logging.error("Error fetching market data: %s", e)
        raise


# Insert market data into DB
def insert_market_data(market_data):
    records = []
    for c in market_data:
        try:
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
                    datetime.fromisoformat(c["last_updated"].replace("Z", "+00:00")),
                )
            )
        except Exception as e:
            logging.warning("Skipping coin due to parsing error: %s", e)

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
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
        logging.info("Inserted %d coin market records into DB", len(records))
    except Exception as e:
        logging.error("Error inserting market data: %s", e)
        raise


# Run as script
if __name__ == "__main__":
    try:
        logging.info("=== Market Data Fetch Job Started ===")
        data = fetch_market_data(per_page=50)
        insert_market_data(data)
        logging.info("=== Market Data Fetch Job Completed ===\n")
    except Exception as e:
        logging.error("Market data fetch job failed: %s", e)
