import pandas as pd
import argparse
import sqlite3
import os
import numpy as np
import re

# We chose a low value of 1 for the privacy budget to guarantee strong privacy due to the sensitivity of the data (STIs)
EPSILON = 1


def date_of_birth(date):
    return 1

def post_code(postal_code):
    return 2

def education_status(education_status):
    return 3

def chlamydia(chlamydia):
    return laplace_mech(chlamydia, 1, 0.1)

def gonorrhea(gonorrhea):
    return laplace_mech(gonorrhea, 1, 0.1)

def syphilis(syphilis):
    return laplace_mech(syphilis, 1, 0.1)


function_map = {
    "Date of Birth": date_of_birth,
    "Postal Code": post_code,
    "Education Status": education_status,
    "Chlamydia": chlamydia,
    "Gonorrhea": gonorrhea,
    "Syphilis": syphilis,
}


def create_function_map(renamed_fields):
    new_function_map = function_map.copy()
    for original, new in renamed_fields:
        new_function_map[new] = new_function_map[
            original.replace('"', "").replace("'", "")
        ]
    return new_function_map


def laplace_mech(v, sensitivity, epsilon):
    return v + np.random.laplace(loc=0, scale=sensitivity / epsilon)


def create_dynamic_class_instance(class_name, field_names, row):
    class_obj = type(class_name, (object,), {})
    instance = class_obj()
    for field_name, value in zip(field_names, row):
        setattr(instance, field_name, value)
    return instance


def execute_query(cursor, query: str):
    try:
        cursor.execute(query)
        query_result = cursor.fetchall()
        pattern = re.compile(
            r'(["\[\]]?[\w\s]+["\[\]]?)\s+AS\s+(\w+)', re.IGNORECASE
        )  # COOKED
        renamed_fields = pattern.findall(query)
        new_function_map = create_function_map(renamed_fields)
        fields = [description[0] for description in cursor.description]
        new_query_result = [
            create_dynamic_class_instance("Row", fields, row) for row in query_result
        ]

        for query in new_query_result:
            for field in fields:
                fun = new_function_map.get(field)
                query.__dict__[field] = fun(query.__dict__[field])
        return new_query_result
    except Exception as e:
        print(e)
        return []


def execute_commands(conn):
    cursor = conn.cursor()
    command = input()
    while command != "exit":
        results = execute_query(cursor, command)
        for row in results:
            print(row.__dict__)
        command = input()


def main(sti_data):
    data = pd.read_csv(sti_data)
    with sqlite3.connect("sti_data.db") as conn:
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
    os.remove("sti_data.db")
