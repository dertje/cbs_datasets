import json
from .dataset import CBSDataSet
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def process_table_info(dataset_name: str):
    try:
        base_url = f"https://opendata.cbs.nl/ODataFeed/odata/{dataset_name}"
        print(f"Processing {dataset_name}")

        dataset = CBSDataSet(base_url)
        table_info = get_table_info_values(dataset)

        print(f"Finished {dataset_name}")
        return table_info
    except Exception as e:
        print(f"Failed {dataset_name}: {e}")
        return None  # Mark as failed

def get_table_info_values(dataset):
    entry = dataset.get_table_info_entry() # TODO add check for if dataset does not have entry (then it should skip it)
    namespaces = dataset.namespaces
    row = {}

    # Top-level elements inside <entry>
    for child in entry:
        tag = child.tag.split('}', 1)[-1]
        if tag == "content":
            # Go deeper into <m:properties>
            properties = child.find('m:properties', namespaces)
            if properties is not None:
                for prop in properties:
                    prop_tag = prop.tag.split('}', 1)[-1]
                    row[prop_tag] = prop.text
        elif child.text and child.text.strip():
            row[tag] = child.text.strip()
        else:
            # Optionally extract attributes (e.g. link href)
            if tag == "link":
                href = child.attrib.get("href")
                if href:
                    row["link"] = href
            elif tag == "category":
                term = child.attrib.get("term")
                if term:
                    row["category"] = term

    return row

def main():
    with open('../output_files/available_datasets.txt', 'r', encoding='utf-8') as file:
        datasets_names = [line.strip() for line in file]

    output_file = "../output_files/tables_infos.json"

    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            all_entries = existing_data.get("entries", [])
    except (json.JSONDecodeError, FileNotFoundError):
        all_entries = []

    max_workers = 10
    print(f"Running in parallel with {max_workers} workers...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_table_info, name): name for name in datasets_names}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing datasets"):
            dataset_name = futures[future]
            try:
                result = future.result()
                if result:
                    all_entries.append(result)
            except Exception as e:
                print(f"Error processing {dataset_name}: {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"entries": all_entries}, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
