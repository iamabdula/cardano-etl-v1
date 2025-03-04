# src/transformation.py

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_to_eur(amount, exchange_rate):
    """
    Converts an amount to EUR using the provided exchange rate.
    """
    try:
        result = float(amount) * float(exchange_rate)
        return result
    except Exception as e:
        logger.error("Error converting to EUR: amount=%s, exchange_rate=%s; Error: %s",
                     amount, exchange_rate, e, exc_info=True)
        raise

def add_eur_column(df):
    """
    Adds an 'amount_in_euros' column to the DataFrame by converting the 'notional' column using the 'exchange_rate' column.
    """
    try:
        df['amount_in_euros'] = df.apply(
            lambda row: convert_to_eur(row['notional'], row['exchange_rate']), axis=1
        )
        logger.info("Successfully added 'amount_in_euros' column to DataFrame.")
        return df
    except Exception as e:
        logger.error("Error adding 'amount_in_euros' column: %s", e, exc_info=True)
        raise
