import requests
import xml.etree.ElementTree as ET

class CBSDataSet:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices',
            'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata',
        }
        self.typed_root = self._fetch_root("/TypedDataSet")
        self.base_root = self._fetch_root("")
        self.table_info_root = self._fetch_root("/TableInfos")

    def _fetch_root(self, suffix: str):
        url = self.base_url + suffix
        response = requests.get(url)
        response.raise_for_status()
        return ET.fromstring(response.content)

    def get_flat_entries(self):
        return self.typed_root.findall('atom:entry', self.namespaces)

    def get_table_info_entry(self):
        return self.table_info_root.find('atom:entry', self.namespaces)

    def get_titles(self):
        return self.base_root.findall(".//atom:title", self.namespaces)

    def get_relational_mapping(self, title):
        mapping = {}
        rel_root = self._fetch_root(f"/{title}")
        entries = rel_root.findall('atom:entry', self.namespaces)
        for entry in entries:
            key_elem = entry.find('atom:content/m:properties/d:Key', self.namespaces)
            val_elem = entry.find('atom:content/m:properties/d:Title', self.namespaces)
            if key_elem is not None and val_elem is not None:
                mapping[key_elem.text] = val_elem.text
        return mapping
