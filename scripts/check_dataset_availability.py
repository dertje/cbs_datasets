import requests
from fetch import get_datasets_names

# TODO add dataderden available datasets

def filter_non_available_datasets(datasets_names):
    valid_datasets = []
    nb_datasets_left = len(datasets_names)
    for name in datasets_names:
        print(f"Running dataset {name}")
        # url = f"https://opendata.cbs.nl/ODataFeed/odata/{name}"
        url = f"https://dataderden.cbs.nl/ODataFeed/OData/{name}"
        try:
            response = requests.get(url, timeout=5)
            if "vervallen" not in response.text.lower():
                valid_datasets.append(name)
            elif "TijdelijkNietBeschikbaar" not in response.text.lower(): # TODO check if this extra statement works
                valid_datasets.append(name)
            else:
                print(f"Skipping {name}: dataset no longer available.")
        except Exception as e:
            print(f"Skipping {name}: failed to fetch ({e})")

        nb_datasets_left -= 1
        print(f"number of datasets to run left: {nb_datasets_left}")

    return valid_datasets

def main():
    # index_url = "https://opendata.cbs.nl/odatafeed"
    index_url = "https://dataderden.cbs.nl/odatafeed"
    print(index_url)
    datasets_names = get_datasets_names(index_url)
    available_datasets_names = filter_non_available_datasets(datasets_names)

    with open('../output_files/available_datasets_derden.txt', 'w') as file:
        file.write("\n".join(available_datasets_names))


if __name__ == '__main__':
    main()

