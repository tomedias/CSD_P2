import pandas as pd
import argparse
import numpy as np
import matplotlib.pyplot as plt


def isKAnonymized(df, k):
    for index, row in df.iterrows():
        query_parts = []
        for col in df.columns:
            value = row[col]
            if pd.isna(value):
                query_parts.append(f'`{col}`.isna()')
            elif isinstance(value, str):
                query_parts.append(f'`{col}` == "{value}"')
            elif isinstance(value, bool):
                query_parts.append(f'`{col}` == {value}')
            else:
                query_parts.append(f'`{col}` == {value}')
        query = ' & '.join(query_parts)
        try:
            rows = df.query(query)
        except Exception as e:
            print(f"Query failed: {query}")
            print(e)
            return False
        if rows.shape[0] < k:
            return False
    return True


data = pd.read_csv("sti_data_anon.csv")
print(data.columns)

if isKAnonymized(data, 2):
      print("All good")
else:
    print("Womp Womp")
