import logging

from psycopg2.extras import execute_values

from config.db_config import get_connection


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
