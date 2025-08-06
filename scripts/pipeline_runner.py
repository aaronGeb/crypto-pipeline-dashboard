#!/usr/bin/env python3
import logging

from scripts.fetch_coin import fetch_coins
from scripts.fetch_coin_market_data import fetch_market_data
from scripts.insert_coins import insert_coins
from scripts.insert_market_data import insert_market_data

# Setup logging
logging.basicConfig(
    filename="logs/pipeline_runner.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def main():
    logging.info("=== Pipeline Run Started ===")
    try:
        # Step 1: Fetch and insert coin metadata
        coins = fetch_coins()
        logging.info("Fetched %d coins", len(coins))
        insert_coins(coins)
        logging.info("Inserted coin metadata successfully")

        # Step 2: Fetch and insert market data
        market_data = fetch_market_data(per_page=50)
        logging.info("Fetched market data for %d coins", len(market_data))
        insert_market_data(market_data)
        logging.info("Inserted market data successfully")

        logging.info("=== Pipeline Run Completed ===\n")

    except Exception as e:
        logging.error("Pipeline failed: %s", e)


if __name__ == "__main__":
    main()
