import csv

def table_without_relational_values(dataset, csv_file_name):
    entries = dataset.get_flat_entries()
    data = []
    fieldnames = []

    for i, entry in enumerate(entries):
        properties = entry.find('atom:content/m:properties', dataset.namespaces)
        row = {}
        if properties is not None:
            if i == 0:
                fieldnames = [elem.tag.split('}', 1)[-1] for elem in properties]
            for elem in properties:
                tag = elem.tag.split('}', 1)[-1]
                row[tag] = elem.text
            data.append(row)

    with open(csv_file_name, mode='w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(data)

    return fieldnames
