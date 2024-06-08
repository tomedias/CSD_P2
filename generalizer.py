import pandas as pd
import argparse
import numpy as np
import matplotlib.pyplot as plt


def generalize_year(date_str):
    day, month, year = date_str.split("/")
    generalized_date = f"00/{month}/{year}"
    new_year = round(int(year) / 10) * 10
    generalized_date = generalized_date.replace(year, str(new_year))

    return generalized_date


def generalize_year2(date_str):
    day, month, year = date_str.split("/")
    generalized_date = f"00/{month}/{year}"
    new_year = round(int(year) / 50) * 50
    generalized_date = generalized_date.replace(year, str(new_year))

    return generalized_date


def generalize_month(date_str):
    day, month, year = date_str.split("/")
    generalized_date = f"00/{month}/{year}"
    new_month = old_month = int(month)
    if 1 <= old_month <= 3:
        new_month = "01"
    elif 4 <= old_month <= 6:
        new_month = "02"
    elif 7 <= old_month <= 9:
        new_month = "03"
    elif 10 <= old_month <= 12:
        new_month = "04"
    generalized_date = generalized_date.replace(month, str(new_month))

    return generalized_date


def generalize_education(status):
    if status in range(1, 9):
        return 1
    elif status in range(9, 17):
        return 2
    else:
        return 2


def generalize(df):
    df["Education Status"] = df["Education Status"].astype(int)
    df["Education Status"] = df["Education Status"].apply(generalize_education)

    df["Date of Birth"] = df["Date of Birth"].apply(generalize_year2)
    df["Date of Birth"] = df["Date of Birth"].apply(generalize_month)
    df["Postal Code"] = df["Postal Code"].astype(str)
    df["Postal Code"] = df["Postal Code"].apply(lambda x: x[:2] + "XX")


data = pd.read_csv("sti_data.csv")
generalize(data)
output_path = "./sti_data_anon.csv"
data.to_csv(output_path, index=False)
