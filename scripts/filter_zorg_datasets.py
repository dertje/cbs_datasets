from dataset import CBSDataSet
import time

def get_dataset_theme(dataset_name):
    base_url = f"https://opendata.cbs.nl/ODataFeed/odata/{dataset_name}"
    dataset = CBSDataSet(base_url)
    entry = dataset.get_table_info_entry()

    if entry is None:
        return False
    else:
        namespaces = dataset.namespaces

        description = entry.find('atom:content/m:properties/d:Description', namespaces).text
        gezondheid_en_welzijn = "https://www.cbs.nl/nl-nl/maatschappij/gezondheid-en-welzijn"
        if gezondheid_en_welzijn in description:
            print(f"dataset {dataset_name} is van de zorg.")
            return True
        else:
            print(f"dataset {dataset_name} is niet van de zorg.")
            return False

def main():
    start = time.time()
    with open('../output_files/available_datasets.txt', 'r', encoding='utf-8') as file:
        datasets_names = [line.strip() for line in file]

    zorg_datasets_names = []
    nb_datasets_left = len(datasets_names)
    for dataset_name in datasets_names:
        print(f"Running dataset {dataset_name}")
        if get_dataset_theme(dataset_name):
            zorg_datasets_names.append(dataset_name)
        nb_datasets_left -= 1
        print(f"number of datasets to run left: {nb_datasets_left}")
    
    print(f"{len(zorg_datasets_names)} zorg datasets found.")
    
    with open('../output_files/available_zorg_datasets.txt', 'w') as file:
        file.write("\n".join(zorg_datasets_names))
    
    end = time.time()
    print(f"All datasets checked for zorg datasets in {end - start:.2f}s.")


if __name__ == '__main__':
    main()
