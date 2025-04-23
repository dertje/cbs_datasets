import time
from concurrent.futures import ThreadPoolExecutor
from process import process_dataset
from tqdm import tqdm

# TODO Add documentation
# TODO also use dataderden?

def main():
    start = time.time()

    # # Load all datasets
    with open('../output_files/available_datasets.txt', 'r', encoding='utf-8') as file:
        datasets_names = [line.strip() for line in file]

    datasets_names = ['03727']
    max_workers = 10
    print(f"Running in parallel with {max_workers} workers...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(tqdm(executor.map(process_dataset, datasets_names), total=len(datasets_names), desc="Processing datasets"))

    end = time.time()
    print(f"All datasets processed in {end - start:.2f}s")

if __name__ == '__main__':
    main()
