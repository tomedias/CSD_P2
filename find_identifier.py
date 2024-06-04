import pandas as pd
import os


def get_identifier(data: pd.DataFrame):
    for collumn_name, collumn_data in data.items():
        if len(set(collumn_data)) == len(collumn_data):
            return collumn_name
    return None


directory_path = os.path.curdir

csv_files = [
    os.path.join(directory_path, filename)
    for filename in os.listdir(directory_path)
    if filename.endswith(".csv")
]
identifiers = []

for file in csv_files:
    data = pd.read_csv(file)
    identifier = get_identifier(data)
    if identifier:
        identifiers.append(identifier)
