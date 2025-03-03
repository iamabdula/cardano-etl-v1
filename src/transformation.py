# utility functions for Transformatio
def convert_to_eur(amount, exchange_rate):
    return float(amount) * float(exchange_rate)

def add_eur_column(df):
    df['amount_in_euros'] = df.apply(
        lambda row: convert_to_eur(row['notional'], row['exchange_rate']), axis=1
    )
    return df