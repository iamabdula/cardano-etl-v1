# src/main.py

import os
import logging
import pandas as pd

from ingestion import read_csv, read_json, read_xml
from transformation import add_eur_column
from storage import store_in_sqlite, save_to_csv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_data(csv_file, json_file, xml_file):
    try:
        df_csv = read_csv(csv_file)
        df_json = read_json(json_file)
        df_xml = read_xml(xml_file)

        # Process each dataset by adding the EUR conversion column
        df_csv = add_eur_column(df_csv)
        df_json = add_eur_column(df_json)
        df_xml = add_eur_column(df_xml)

        # Combine all the datasets into a single DataFrame
        df_all = pd.concat([df_csv, df_json, df_xml], ignore_index=True)
        logger.info("Successfully processed data from CSV, JSON, and XML.")
        return df_all

    except Exception as e:
        logger.error("Error processing data: %s", e, exc_info=True)
        raise

if __name__ == "__main__":
    # Define the directory where the data files reside inside the container
    data_dir = "/app/data"
    logger.info("Current working directory: %s", os.getcwd())

    if os.path.exists(data_dir):
        logger.info("Contents of %s: %s", data_dir, os.listdir(data_dir))
    else:
        logger.error("The directory %s does not exist!", data_dir)

    # Define full file paths for the input files
    csv_file = os.path.join(data_dir, "input_dataset_csv.csv")
    json_file = os.path.join(data_dir, "input_dataset_json.json")
    xml_file = os.path.join(data_dir, "input_dataset_xml.xml")

    logger.info("CSV file path: %s", os.path.abspath(csv_file))
    logger.info("JSON file path: %s", os.path.abspath(json_file))
    logger.info("XML file path: %s", os.path.abspath(xml_file))

    try:
        df = process_data(csv_file, json_file, xml_file)
        store_in_sqlite(df)
        save_to_csv(df)
        logger.info("Data processing and storage complete.")
    except Exception as e:
        logger.error("Pipeline failed: %s", e, exc_info=True)
