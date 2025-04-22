import time
from concurrent.futures import ThreadPoolExecutor
from process import process_dataset

# TODO Add documentation
# TODO also use dataderden?

def main():
    start = time.time()

    # # Load all datasets
    with open('../output_files/available_datasets.txt', 'r', encoding='utf-8') as file:
        datasets_names = [line.strip() for line in file]

    # # Only load 'zorg' classified datasets
    # with open('../output_files/available_zorg_datasets.txt', 'r', encoding='utf-8') as file:
    #     zorg_datasets_names = [line.strip() for line in file]

    max_workers = 5
    print(f"Running in parallel with {max_workers} workers...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_dataset, datasets_names)
        # executor.map(process_dataset, zorg_datasets_names)

    end = time.time()
    print(f"All datasets processed in {end - start:.2f}s")

if __name__ == '__main__':
    main()
