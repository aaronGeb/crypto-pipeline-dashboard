import logging
from datetime import datetime

from psycopg2.extras import execute_values

from config.db_config import get_connection


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
            logging.warning("Skipping record due to parsing error: %s", e)

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
