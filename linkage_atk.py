import pandas as pd
import argparse


def main(marriage_file, earning_file, sti_file):
    marriage_data = pd.read_csv("marriage_data.csv")
    earning_data = pd.read_csv("earning_data.csv")
    sti_data = pd.read_csv("sti_data.csv")

    merge_earning_sti = pd.merge(
        earning_data, sti_data, on=["Date of Birth", "Education Status"], how="inner"
    )
    merge_all = pd.merge(
        merge_earning_sti, marriage_data, on=["Postal Code", "Occupation"], how="inner"
    )
    # merge_final = pd.merge(merge_earning_sti, marriage_data, on=['Postal Code'],how='inner')
    nif_count = merge_all["NIF"].value_counts()
    # nif_count.hist()
    # plt.show()

    merge_final = merge_all[merge_all["NIF"].isin(nif_count[nif_count == 1].index)]

    output_path1 = "./unique_data.csv"
    output_path2 = "./reidentified.csv"
    merge_final.to_csv(output_path1, index=False)
    merge_all.to_csv(output_path2, index=False)
    print(f"Saved results to {output_path1} and {output_path2}")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Linkage Attack.")
    parser.add_argument("marriage_file", help="Path to the marriage data file.")
    parser.add_argument("earning_file", help="Path to the earning datafile.")
    parser.add_argument("sti_file", help="Path to the STI data file.")

    # Parse arguments
    args = parser.parse_args()

    # Call main function with parsed arguments
    main(args.marriage_file, args.earning_file, args.sti_file)
