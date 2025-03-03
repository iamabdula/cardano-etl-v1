import sqlite3

def store_in_sqlite(df, db_file="output.db"):
    conn = sqlite3.connect(db_file)
    df.to_sql("transactions", conn, if_exists="replace", index=False)
    conn.close()
