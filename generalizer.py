import pandas as pd
import argparse

def generalize_day(date_str):
    day, month, year = date_str.split("/")
    new_day = day
    old_day = int(day)
    if 1 <= old_day <= 15:
        new_day = "15"
    elif 16 <= old_day <= 31:
        new_day = "30"
    
    generalized_date = f"{new_day}/{month}/{year}"

    return generalized_date

def generalize_day2(date_str):
    _, month, year = date_str.split("/")
    generalized_date = f"00/{month}/{year}"

    return generalized_date

def generalize_day6(date_str):
    day, month, year = date_str.split("/")
    new_day = day
    old_day = int(day)
    if 1 <= old_day <= 10:
        new_day = "10"
    elif 11 <= old_day <= 20:
        new_day = "20"
    else:
        new_day = "30"
    
    generalized_date = f"{new_day}/{month}/{year}"

    return generalized_date

def generalize_year(date_str):
    day, month, year = date_str.split("/")
    generalized_date = f"{day}/{month}/{year}"
    new_year = round(int(year) / 10) * 10
    generalized_date = generalized_date.replace(year, str(new_year))

    return generalized_date

def generalize_year6(date_str):
    day, month, year = date_str.split("/")
    generalized_date = f"{day}/{month}/{year}"
    new_year = round(int(year) / 2) * 2
    generalized_date = generalized_date.replace(year, str(new_year))

    return generalized_date

def generalize_year3(date_str):
    day, month, year = date_str.split("/")
    generalized_date = f"{day}/{month}/{year}"
    new_year = round(int(year) / 25) * 25
    generalized_date = generalized_date.replace(year, str(new_year))

    return generalized_date


def generalize_year2(date_str):
    day, month, year = date_str.split("/")
    generalized_date = f"{day}/{month}/{year}"
    new_year = round(int(year) / 50) * 50
    generalized_date = generalized_date.replace(year, str(new_year))

    return generalized_date

def generalize_month3(date_str):
    day, month, year = date_str.split("/")
    generalized_date = f"{day}/{month}/{year}"
    new_month = old_month = int(month)
    if 1 <= old_month <= 6:
        new_month = "01"
    elif 7 <= old_month <= 12:
        new_month = "02"

    generalized_date = generalized_date.replace(month, str(new_month))

    return generalized_date

def generalize_month6(date_str):
    day, month, year = date_str.split("/")
    generalized_date = f"{day}/{month}/{year}"
    new_month = old_month = int(month)
    if old_month <= 6:
        new_month = "01"
    else:
        new_month = "02"
    generalized_date = generalized_date.replace(month, str(new_month))

    return generalized_date

def generalize_month(date_str):
    day, month, year = date_str.split("/")
    generalized_date = f"{day}/{month}/{year}"
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

def generalize_month2(date_str):
    day , month, year = date_str.split("/")
    generalized_date = f"{day}/{month}/{year}"
    new_month = old_month = int(month)
    if 1 <= old_month <= 2:
        new_month = "01"
    elif 3 <= old_month <= 4:
        new_month = "02"
    elif 5 <= old_month <= 6:
        new_month = "03" 
    elif 7 <= old_month <= 8:
        new_month = "04"       
    elif 9 <= old_month <= 10:
        new_month = "05"
    elif 11 <= old_month <= 12:
        new_month = "06"
    generalized_date = generalized_date.replace(month, str(new_month))

    return generalized_date
    
def generalize_education(status):
    if status in range(1, 9):
        return 1
    elif status in range(10, 12):
        return 2
    elif status in range(13, 16):
        return 3
    else:
        return 3
    
def generalize_education2(status):
    if status in range(1, 12):
        return 1
    elif status in range(13, 16):
        return 2
    else:
        return 2
    
def generalize_education3(status):
    if status in range(1, 9):
        return 1
    return 2
    
def generalize2(df):
    df["Education Status"] = df["Education Status"].astype(int)
    df["Education Status"] = df["Education Status"].apply(generalize_education3)

    df["Date of Birth"] = df["Date of Birth"].apply(generalize_month6)
    df["Date of Birth"] = df["Date of Birth"].apply(generalize_day6)

    df["Postal Code"] = df["Postal Code"].astype(str)
    df["Postal Code"] = df["Postal Code"].apply(lambda x: "XXXX")
    #df["Postal Code"] = df["Postal Code"].apply(lambda x: x[:2] + "XX")
    
def generalize3(df):
    df["Education Status"] = df["Education Status"].astype(int)
    
    df["Education Status"] = df["Education Status"].apply(generalize_education)

    df["Date of Birth"] = df["Date of Birth"].apply(generalize_year2)
    df["Date of Birth"] = df["Date of Birth"].apply(generalize_month)
    df["Date of Birth"] = df["Date of Birth"].apply(generalize_day)

    df["Postal Code"] = df["Postal Code"].astype(str)
    df["Postal Code"] = df["Postal Code"].apply(lambda x: x[:2] + "XX")

def generalize4(df):
    df["Education Status"] = df["Education Status"].astype(int)
    df["Education Status"] = df["Education Status"].apply(generalize_education)

    df["Date of Birth"] = df["Date of Birth"].apply(generalize_year2)
    df["Date of Birth"] = df["Date of Birth"].apply(generalize_month2)
    df["Date of Birth"] = df["Date of Birth"].apply(generalize_day2)

    df["Postal Code"] = df["Postal Code"].astype(str)
    df["Postal Code"] = df["Postal Code"].apply(lambda x: x[:2] + "XX")

def generalize5(df):
    df["Education Status"] = df["Education Status"].astype(int)
    df["Education Status"] = df["Education Status"].apply(generalize_education)

    df["Date of Birth"] = df["Date of Birth"].apply(generalize_year2)
    df["Date of Birth"] = df["Date of Birth"].apply(generalize_month2)
    df["Date of Birth"] = df["Date of Birth"].apply(generalize_day2)
    df["Postal Code"] = df["Postal Code"].astype(str)
    df["Postal Code"] = df["Postal Code"].apply(lambda x: x[:2] + "XX")



def main(sti_data,k):
    data = pd.read_csv(sti_data)
    match k:
        case 2:
         generalize2(data)
        case 3:
         generalize3(data)
        case 4:
         generalize4(data)
        case 5:
         generalize5(data)
        case _:
            print("Please use a k in range 2-5")
    output_path = "./data_anon.csv"
    data.to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generalizer.")
    parser.add_argument("sti_data", help="Path to the sti_data file to generalize.")
    parser.add_argument("k_value", help="K value to test.")
    args = parser.parse_args()
    main(args.sti_data,int(args.k_value))
