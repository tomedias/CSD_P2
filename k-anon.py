import argparse
import pandas as pd


def isKAnonymized(df, k):
    quasi_ids = ["Date of Birth", "Postal Code", "Education Status"]
    unique_entries = []
    for _, row in df.iterrows():
        query_parts = []
        for col in quasi_ids:
            value = row[col]
            if pd.isna(value):
                query_parts.append(f"`{col}`.isna()")
            elif isinstance(value, str):
                query_parts.append(f'`{col}` == "{value}"')
            elif isinstance(value, bool):
                query_parts.append(f"`{col}` == {value}")
            else:
                query_parts.append(f"`{col}` == {value}")
        query = " & ".join(query_parts)
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


def main(data_file, k_value):
    data = pd.read_csv(data_file)
    print(data.columns)

    if isKAnonymized(data, int(k_value)):
        print("All good")
    else:
        print("Womp Womp")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="K-Anonymizer.")
    parser.add_argument("original_file", help="Path to the data file to anonymize.")
    parser.add_argument("k_value")

    # Parse arguments
    args = parser.parse_args()

    # Call main function with parsed arguments
    main(args.original_file, args.k_value)
