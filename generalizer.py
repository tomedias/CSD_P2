import pandas as pd
import argparse
import numpy as np
import matplotlib.pyplot as plt


def generalize_date(date_str):
    day, month, year = date_str.split('/')
    generalized_date = f"00/{month}/{year}"
    new_year= round(int(year) / 10) * 10
    generalized_date = generalized_date.replace(year, str(new_year))

    return generalized_date


def generalize_education(status):
    if status in range(1, 5):
        return 4
    elif status in range(5, 9):
        return 8
    elif status in range(9, 13):
        return 12
    elif status in range(13, 17):
        return 16
    else:
        return status

def generalize(df):
    df['Date of Birth'] = df['Date of Birth'].apply(generalize_date)
    df['Postal Code'] = df['Postal Code'].astype(str)
    df['Postal Code'] = df['Postal Code'].apply(lambda x: x[:2] + 'XX')
    df['Education Status'] = df['Education Status'].astype(int)
    df['Education Status'] = df['Education Status'].apply(generalize_education)


data = pd.read_csv("sti_data.csv")
generalize(data)
output_path = "./sti_data_anon.csv"
data.to_csv(output_path, index=False)
