import pandas as pd

def isKAnonymized(df, k):
    quasi_ids = ['Date of Birth', 'Postal Code', 'Education Status']
    unique_entries = []
    for index, row in df.iterrows():
        query_parts = []
        for col in quasi_ids:
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
            unique_entries.append(row)
    if unique_entries:
        print("Unique entries that do not meet k-anonymity:")
        for entry in unique_entries:
            print(entry)
        return False
    return True


data = pd.read_csv("sti_data_anon.csv")
print(data.columns)

if isKAnonymized(data, 5):
      print("All good")
else:
    print("Womp Womp")
