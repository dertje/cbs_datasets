import requests
from bs4 import BeautifulSoup
import re

def get_datasets_names(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    dataset_links = soup.find_all("a", href=True)
    dataset_names = []

    for link in dataset_links:
        match = re.search(r'/ODataFeed/OData/([^/]+)', link['href'])
        if match:
            dataset_names.append(match.group(1).strip())

    return dataset_names
