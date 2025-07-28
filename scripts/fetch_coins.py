import logging
import os

import psycopg2
import requests
from dotenv import load_dotenv
from psycopg2.extras import execute_values

# Load .env variables
load_dotenv()

# Configure logging
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "fetch_coin.log")
logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

# DB connection config
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
}


# Connect to PostgreSQL
def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        logging.error("DB connection failed: %s", e)
        raise


# Fetch list of all coins
def fetch_coins():
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("Fetched %d coins from CoinGecko", len(response.json()))
        return response.json()
    except Exception as e:
        logging.error("Error fetching coins: %s", e)
        raise


# Insert coins into DB
def insert_coins(coins):
    try:
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
        logging.info("Inserted %d new coins into DB", len(coins))
    except Exception as e:
        logging.error("Error inserting coins: %s", e)
        raise


if __name__ == "__main__":
    try:
        logging.info("=== Coin Fetch Job Started ===")
        coins = fetch_coins()
        insert_coins(coins)
        logging.info("=== Coin Fetch Job Completed Successfully ===\n")
    except Exception as e:
        logging.error("Coin fetch job failed: %s", e)
