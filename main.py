import pandas as pd

marriage_data = pd.read_csv("marriage_data.csv")
earning_data = pd.read_csv("earning_data.csv")
sti_data = pd.read_csv("sti_data.csv")

merge_earning_sti = pd.merge(earning_data, sti_data, on=['Date of Birth','Education Status'],how='inner')
merge_all = pd.merge(merge_earning_sti, marriage_data, on=['Postal Code','Occupation'],how='inner')
#merge_final = pd.merge(merge_earning_sti, marriage_data, on=['Postal Code'],how='inner')
nif_count = merge_all['NIF'].value_counts()
merge_final = merge_all[merge_all['NIF'].isin(nif_count[nif_count==1].index)]

output_path = "./merge_final_data.csv"
merge_final.to_csv(output_path, index=False)

