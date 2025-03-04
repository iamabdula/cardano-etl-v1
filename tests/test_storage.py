import os
import sqlite3
import pandas as pd
import pytest
from src.storage import store_in_sqlite, save_to_csv

def test_store_in_sqlite(tmp_path):
    # Create a sample DataFrame.
    df = pd.DataFrame({"a": [1, 2, 3]})
    db_file = tmp_path / "test.db"
    
    # Store data in SQLite.
    store_in_sqlite(df, db_file=str(db_file))
    
    # Verify that the table exists and contains the expected rows.
    conn = sqlite3.connect(str(db_file))
    cursor = conn.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    
    assert len(rows) == 3

def test_save_to_csv(tmp_path):
    # Create a sample DataFrame.
    df = pd.DataFrame({"a": [1, 2, 3]})
    csv_file = tmp_path / "test_output.csv"
    
    # Save to CSV.
    save_to_csv(df, output_file=str(csv_file))
    
    # Read back the file and compare.
    df_loaded = pd.read_csv(str(csv_file))
    pd.testing.assert_frame_equal(df, df_loaded)
