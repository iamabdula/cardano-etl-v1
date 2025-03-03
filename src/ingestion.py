# src/ingestion.py

import pandas as pd
import json
import xml.etree.ElementTree as ET

def read_csv(file_path):
    """
    Reads a tab-delimited CSV file and standardizes the header for the legal entity identifier to 'lei'.
    """
    try:
        df = pd.read_csv(file_path, sep=",")
        if 'legal_entity_identifier' in df.columns:
            df.rename(columns={'legal_entity_identifier': 'lei'}, inplace=True)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return pd.DataFrame()

def read_json(file_path):
    """
    Reads a JSON file 
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        transactions = data.get("transactions", [])
        df = pd.DataFrame(transactions)
        return df
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return pd.DataFrame()

def read_xml(file_path):
    """
    Reads an XML file 
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        records = []
        for transaction in root.findall("transaction"):
            record = {}
            for child in transaction:
                # Use child.tag as key and child.text as value.
                record[child.tag] = child.text
            records.append(record)
        df = pd.DataFrame(records)
        return df
    except Exception as e:
        print(f"Error reading XML file: {e}")
        return pd.DataFrame()

# For testing the functions locally
if __name__ == "__main__":
    csv_file = "./data/input_dataset_csv.csv"
    json_file = "./data/input_dataset_json.json"
    xml_file = "./data/input_dataset_xml.xml"
    
    df_csv = read_csv(csv_file)
    print("CSV Data:")
    print(df_csv.head(), "\n")
    
    df_json = read_json(json_file)
    print("JSON Data:")
    print(df_json.head(), "\n")
    
    df_xml = read_xml(xml_file)
    print("XML Data:")
    print(df_xml.head(), "\n")
