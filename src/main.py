from ingestion import read_csv, read_json, read_xml
from transformation import add_eur_column
from storage import store_in_sqlite
import pandas as pd

def process_data(csv_file, json_file, xml_file):
    df_csv = read_csv(csv_file)
    df_json = read_json(json_file)
    df_xml = read_xml(xml_file)

    # Process each dataset
    df_csv = add_eur_column(df_csv)
    df_json = add_eur_column(df_json)
    df_xml = add_eur_column(df_xml)

    # Combine the datasets
    df_all = pd.concat([df_csv, df_json, df_xml], ignore_index=True)
    return df_all

if __name__ == "__main__":
    csv_file = "./data/input_dataset_csv.csv"
    json_file = "./data/input_dataset_json.json"
    xml_file = "./data/input_dataset_xml.xml"

    df = process_data(csv_file, json_file, xml_file)
    store_in_sqlite(df)
    print("Data processing and storage complete.")
