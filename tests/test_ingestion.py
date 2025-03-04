import io
import json
import xml.etree.ElementTree as ET
import pandas as pd
import pytest
from src.ingestion import read_csv, read_json, read_xml

def test_read_csv(tmp_path):
    # Create a temporary CSV file with a header that needs renaming.
    csv_content = "legal_entity_identifier,notional,exchange_rate\n" \
                  "ABC,100,0.85\n" \
                  "DEF,200,0.90"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)
    
    df = read_csv(str(csv_file))
    # Verify that the column was renamed to 'lei'
    assert 'lei' in df.columns
    # Verify the DataFrame is not empty and has expected values.
    assert not df.empty
    assert df.loc[0, 'notional'] == 100

def test_read_json(tmp_path):
    # Create a temporary JSON file.
    json_content = {
        "transactions": [
            {"notional": 100, "exchange_rate": 0.85},
            {"notional": 200, "exchange_rate": 0.90}
        ]
    }
    json_file = tmp_path / "test.json"
    json_file.write_text(json.dumps(json_content))
    
    df = read_json(str(json_file))
    # Verify the DataFrame is not empty and has expected keys.
    assert not df.empty
    assert "notional" in df.columns

def test_read_xml(tmp_path):
    # Create a temporary XML file.
    xml_content = """<?xml version="1.0"?>
    <transactions>
        <transaction>
            <notional>100</notional>
            <exchange_rate>0.85</exchange_rate>
        </transaction>
        <transaction>
            <notional>200</notional>
            <exchange_rate>0.90</exchange_rate>
        </transaction>
    </transactions>
    """
    xml_file = tmp_path / "test.xml"
    xml_file.write_text(xml_content)
    
    df = read_xml(str(xml_file))
    # Verify that the DataFrame is not empty and contains expected data.
    assert not df.empty
    assert "notional" in df.columns
