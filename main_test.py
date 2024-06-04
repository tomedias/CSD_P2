import pandas as pd


marriage_data = pd.read_csv("marriage_data.csv")
earning_data = pd.read_csv("earning_data.csv")
sti_data = pd.read_csv("sti_data.csv")


merged_data_1 = earning_data.merge(
    sti_data, on=["Date of Birth", "Education Status"], how="inner"
)

merged_data_2 = marriage_data.merge(sti_data, on=["Postal Code"], how="inner")


merged_data_3 = marriage_data.merge(earning_data, on=["Occupation"], how="inner")

print(merged_data_1.columns)
print(merged_data_2.columns)
print(merged_data_3.columns)
joined_merge = merged_data_2.merge(
    merged_data_3,
    on=["NIF", "Occupation", "Marital Status", "Date of Birth", "Education Status"],
    how="inner",
)
print(joined_merge.columns)
# final_merged_data = merged_data_1.merge(merged_data_2, on=["NIF"], how="inner")
# print(final_merged_data.columns)
# final_merged_data = final_merged_data.merge(
# merged_data_3,
# on=["Postal Code", "Date of Birth", "Education Status", "Occupation"],
# )


output_path = "./merged_data.csv"
joined_merge.to_csv(output_path, index=False)
