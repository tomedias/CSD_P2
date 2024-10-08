import argparse
import os
import numpy as np
import re
import pandas as pd
import sqlite3
from datetime import datetime

# We chose a low value of 1 for the privacy budget to guarantee strong privacy due to the sensitivity of the data (STIs information)
EPSILON = 1.0
DATE_FORMAT = "%d/%m/%Y"

class Sensitivity:
    POSTAL_CODE_SENSITIVITY = 3000
    EDUCATION_STATUS_SENSITIVITY = 16
    YEAR_SENSITIVITY = 99  # 2049 - 1950
    DAY_SENSITIVITY = 30  # 31 - 1
    MONTH_SENSITIVITY = 11  # 12 - 1
    DECEASE_SENSITIVITY = 1  # 1 - 0


def expended_budget(epsilon):
    global EPSILON
    if EPSILON <= 0.0:
        raise Exception("Budget exceeded")
    if (EPSILON - epsilon) < 0.0:
        raise Exception("Budget exceeded")


def calculate_sensitivity(data):
    return data.max() - data.min()


def laplace_mech(v, sensitivity, epsilon):
    global EPSILON
    expended_budget(epsilon)
    EPSILON -= epsilon
    return v + np.random.laplace(loc=0, scale=sensitivity / epsilon)


def date_of_birth(date):
    date_object = datetime.strptime(date, DATE_FORMAT)
    new_day = laplace_mech(date_object.day < 0, Sensitivity.DAY_SENSITIVITY, 1)
    new_month = laplace_mech(date_object.month, Sensitivity.MONTH_SENSITIVITY, 1)
    new_year = laplace_mech(date_object.year, Sensitivity.YEAR_SENSITIVITY, 1)
    return "{}/{}/{}".format(int(new_day), int(new_month), int(new_year))


def post_code(postal_code):
    return laplace_mech(postal_code, Sensitivity.POSTAL_CODE_SENSITIVITY, 1)


def education_status(education_status):
    return laplace_mech(education_status, Sensitivity.EDUCATION_STATUS_SENSITIVITY, 1)


def chlamydia(chlamydia):
    return laplace_mech(chlamydia, Sensitivity.DECEASE_SENSITIVITY, 0.1)


def gonorrhea(gonorrhea):
    return laplace_mech(gonorrhea, Sensitivity.DECEASE_SENSITIVITY, 0.1)


def syphilis(syphilis):
    return laplace_mech(syphilis, Sensitivity.DECEASE_SENSITIVITY, 0.1)


def sum_decease(value):
    return laplace_mech(value, Sensitivity.DECEASE_SENSITIVITY, 0.1)


def sum_education_status(value):
    return laplace_mech(value, Sensitivity.EDUCATION_STATUS_SENSITIVITY, 0.1)


def sum_postal_code(value):
    return laplace_mech(value, Sensitivity.POSTAL_CODE_SENSITIVITY, 0.15)#budget allows 6 sequential sums


def count(value):
    return laplace_mech(value, 1, 0.15)#budget allows 6 sequential counts


def avg_decease(sum, count_value):
    return sum_decease(sum) / count(count_value)#budget for this operation allows 4 sequential averages


def avg_education_status(sum, count_value):
    return sum_education_status(sum) / count(count_value)


def avg_postal_code(sum, count_value):
    return sum_postal_code(sum) / count(count_value)


function_map = {
    "Date of Birth": date_of_birth,
    "Postal Code": post_code,
    "Education Status": education_status,
    "Chlamydia": chlamydia,
    "Gonorrhea": gonorrhea,
    "Syphilis": syphilis,
    "Sum(Decease)": sum_decease,
    "Sum(Education Status)": sum_education_status,
    "Sum(Postal Code)": sum_postal_code,
    "Count": count,
    "Avg(Decease)": avg_decease,
    "Avg(Education Status)": avg_education_status,
    "Avg(Postal Code)": avg_postal_code,
}


def create_sum_function(sum_fields, function_map):
    for original in sum_fields:
        if any(
            field.lower() in original.lower().strip()
            for field in ["Chlamydia", "Syphilis", "Gonorrhea"]
        ):
            function_map[original] = sum_decease
        elif "Education Status".lower() in original.lower().strip():
            function_map[original] = sum_education_status
        elif "Postal Code".lower() in original.lower().strip():
            function_map[original] = sum_postal_code


def create_count_function(count_fields, function_map):
    for original in count_fields:
        function_map[original] = count


def create_avg_function(avg_fields, function_map):
    for original in avg_fields:
        if any(
            field.lower() in original.lower().strip()
            for field in ["Chlamydia", "Syphilis", "Gonorrhea"]
        ):
            function_map[original] = avg_decease
        elif "Education Status".lower() in original.lower().strip():
            function_map[original] = avg_education_status
        elif "Postal Code".lower() in avg_fields.lower().strip():
            function_map[original] = avg_postal_code


def create_function_map(renamed_fields):
    new_function_map = function_map.copy()
    for original, new in renamed_fields:
        new_function_map[new] = new_function_map[
            original.replace('"', "").replace("'", "").strip()
        ]
    return new_function_map


def create_dynamic_class_instance(class_name, field_names, row):
    class_obj = type(class_name, (object,), {})
    instance = class_obj()
    for field_name, value in zip(field_names, row):
        setattr(instance, field_name, value)
    return instance


def execute_query(cursor, query: str):
    cursor.execute(query)
    query_result = cursor.fetchall()
    pattern = re.compile(
        r'(["\[\]]?[\w\s]+["\[\]]?)\s+AS\s+(\w+)', re.IGNORECASE
    )  # COOKED
    sum_pattern = re.compile(r"\bSUM\s*\(.*?\)", re.IGNORECASE)
    count_pattern = re.compile(r"\bCOUNT\s*\(.*?\)", re.IGNORECASE)
    avg_pattern = re.compile(r"\bAVG\s*\(.*?\)", re.IGNORECASE)
    renamed_fields = pattern.findall(query)
    sum_pattern = sum_pattern.findall(query)
    count_pattern = count_pattern.findall(query)
    avg_pattern = avg_pattern.findall(query)

    query = query.lower()
    _, fields_and_from = query.split("select")

    _, from_clause = fields_and_from.split("from")

    new_function_map = create_function_map(renamed_fields)
    create_sum_function(sum_pattern, new_function_map)
    create_count_function(count_pattern, new_function_map)
    create_avg_function(avg_pattern, new_function_map)
    fields = [description[0] for description in cursor.description]
    new_query_result = [
        create_dynamic_class_instance("Row", fields, row) for row in query_result
    ]

    for query in new_query_result:
        for field in fields:
            if "avg" in field.lower():
                new_field = (
                    field.lower()
                    .replace("avg", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace('"', "")
                    .replace("'", "")
                    .strip()
                )
                cursor.execute(
                    "SELECT SUM({}), COUNT({}) FROM {}".format(
                        new_field, new_field, from_clause
                    )
                )
                result = cursor.fetchall()
                sum, count = result[0]
                fun = new_function_map.get(field)
                query.__dict__[field] = fun(sum, count)
            else:
                fun = new_function_map.get(field)
                query.__dict__[field] = fun(query.__dict__[field])
    return new_query_result


def execute_commands(conn):
    cursor = conn.cursor()
    command = input()
    while command != "exit":
        if(os.path.isfile("sti_data.db")):
            try:
                results = execute_query(cursor, command)
                for row in results:
                    print(row.__dict__)
                command = input()
            except Exception as e:
                print(e)
                conn.close()
                os.remove("sti_data.db")      
        else:
            print(None)
            command = input()
    return
def clip_dataset(data):
    data["Date of Birth"] = pd.to_datetime(
        data["Date of Birth"], format=DATE_FORMAT, errors="coerce"
    )
    lower_bound = pd.to_datetime("01/01/1950", format="%d/%m/%Y")
    upper_bound = pd.to_datetime("31/12/2049", format="%d/%m/%Y")
    data["Date of Birth"] = data["Date of Birth"].clip(
        lower=lower_bound, upper=upper_bound
    )
    data["Date of Birth"] = data["Date of Birth"].dt.strftime("%d/%m/%Y")
    data["Education Status"] = data["Education Status"].clip(lower=0, upper=16)
    data["Postal Code"] = data["Postal Code"].clip(lower=0, upper=3000)


def main(sti_data):
    
        data = pd.read_csv(sti_data)
        clip_dataset(data)
        conn = sqlite3.connect("sti_data.db")
        data.to_sql("sti", conn, if_exists="replace", index=False)
        execute_commands(conn)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Differential Privacy.")
    parser.add_argument(
        "sti_data",
        help="Path to the sti_data data file.",
    )
    args = parser.parse_args()
    main(args.sti_data)
