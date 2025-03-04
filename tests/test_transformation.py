import pandas as pd
import pytest
from src.transformation import convert_to_eur, add_eur_column

def test_convert_to_eur_valid():
    amount = 100
    exchange_rate = 0.85
    expected = 85.0
    result = convert_to_eur(amount, exchange_rate)
    assert result == expected

def test_convert_to_eur_invalid():
    # Passing a non-numeric value should raise an exception.
    with pytest.raises(Exception):
        convert_to_eur("invalid", 0.85)

def test_add_eur_column():
    # Create a sample DataFrame.
    df = pd.DataFrame({
        'notional': [100, 200, 300],
        'exchange_rate': [0.85, 0.90, 0.80]
    })
    df_result = add_eur_column(df.copy())
    
    # Expected conversion results.
    expected_values = [85.0, 180.0, 240.0]
    # Verify that the column exists.
    assert 'amount_in_euros' in df_result.columns
    # Compare series values.
    pd.testing.assert_series_equal(
        df_result['amount_in_euros'],
        pd.Series(expected_values),
        check_names=False
    )
