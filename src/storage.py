# src/storage.py

import sqlite3
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def store_in_sqlite(df, db_file="output/trans.db"):
    """
    Stores the DataFrame in an SQLite database.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        df.to_sql("transactions", conn, if_exists="replace", index=False)
        logger.info("Data successfully stored in SQLite: %s", db_file)
    except Exception as e:
        logger.error("Error storing data in SQLite: %s", e, exc_info=True)
        raise
    finally:
        if conn:
            conn.close()

def save_to_csv(df, output_file="output/output_csv.csv"):
    """
    Saves the DataFrame to a CSV file.
    """
    try:
        logger.info("Current working directory: %s", os.getcwd())
        if df.empty:
            logger.warning("No data to save in CSV.")
            return

        df.to_csv(output_file, index=False)
        if os.path.exists(output_file):
            logger.info("Output file exists at: %s", output_file)
        logger.info("Data saved to CSV: %s", output_file)
    except Exception as e:
        logger.error("Error saving data to CSV: %s", e, exc_info=True)
        raise
