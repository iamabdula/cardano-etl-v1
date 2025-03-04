# src/ingestion.py

import pandas as pd
import json
import xml.etree.ElementTree as ET
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_csv(file_path):
    """
    Reads a comma-delimited CSV file and standardizes the header for the legal entity identifier to 'lei'.
    """
    try:
        df = pd.read_csv(file_path, sep=",")
        if 'legal_entity_identifier' in df.columns:
            df.rename(columns={'legal_entity_identifier': 'lei'}, inplace=True)
        logger.info(f"Successfully read CSV file: {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error reading CSV file: {file_path}. Error: {e}", exc_info=True)
        return pd.DataFrame()

def read_json(file_path):
    """
    Reads a JSON file.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        transactions = data.get("transactions", [])
        df = pd.DataFrame(transactions)
        logger.info(f"Successfully read JSON file: {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error reading JSON file: {file_path}. Error: {e}", exc_info=True)
        return pd.DataFrame()

def read_xml(file_path):
    """
    Reads an XML file.
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
        logger.info(f"Successfully read XML file: {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error reading XML file: {file_path}. Error: {e}", exc_info=True)
        return pd.DataFrame()

# For testing the functions locally
if __name__ == "__main__":
    csv_file = "./data/input_dataset_csv.csv"
    json_file = "./data/input_dataset_json.json"
    xml_file = "./data/input_dataset_xml.xml"
    
    df_csv = read_csv(csv_file)
    logger.info("CSV Data:")
    logger.info(df_csv.head())
    
    df_json = read_json(json_file)
    logger.info("JSON Data:")
    logger.info(df_json.head())
    
    df_xml = read_xml(xml_file)
    logger.info("XML Data:")
    logger.info(df_xml.head())
