import pandas as pd

def check_relational_values(dataset, fieldnames, csv_file):
    titles = dataset.get_titles()
    titles_found = [field for field in fieldnames if any(field == t.text for t in titles)]

    for title in titles_found:
        replace_value_with_relational(csv_file, dataset, title)

def replace_value_with_relational(csv_file, dataset, title):
    df = pd.read_csv(csv_file, delimiter=';', dtype=str)
    mapping_dict = dataset.get_relational_mapping(title)
    df[title] = df[title].astype(str).replace(mapping_dict)
    df.to_csv(csv_file, index=False, sep=';', encoding='utf-8-sig')
