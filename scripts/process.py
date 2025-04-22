import os
from dataset import CBSDataSet
from extract import table_without_relational_values
from transform import check_relational_values

def process_dataset(dataset_name: str):
    try:
        base_url = f"https://opendata.cbs.nl/ODataFeed/odata/{dataset_name}"
        output_dir = "../output_files/all_datasets"
        os.makedirs(output_dir, exist_ok=True)

        csv_file = f"{output_dir}/{dataset_name}.csv"
        print(f"Processing {dataset_name}")

        dataset = CBSDataSet(base_url)
        fieldnames = table_without_relational_values(dataset, csv_file)
        check_relational_values(dataset, fieldnames, csv_file)

        print(f"Finished {dataset_name}")
    except Exception as e:
        print(f"Failed {dataset_name}: {e}")
