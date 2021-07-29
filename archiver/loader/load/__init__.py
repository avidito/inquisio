import csv
from datetime import datetime

from .engine import get_engine
from .models import TABLE_MODELS

def load_data_to_db(params):
    tmp = params["TMP_PATH"]
    table_list = params["TABLE_LIST"]

    db = get_engine()

    for table_name in table_list:
        header, data = read_data(table_name, tmp)
        truncate_table(db, table_name)
        load_data(db, table_name, header, data)

def read_data(table_name, tmp):
    path = f"{tmp}/prc_{table_name}.csv"
    with open(path, "r") as file:
        reader = csv.reader(file, delimiter=",")
        header, *data = reader
    return header, data


def truncate_table(db, table_name):
    table = TABLE_MODELS[table_name]
    db.query(table).delete()
    db.commit()


def load_data(db, table_name, header, data):
    row_data = [{col: value for col, value in zip(header, row)} for row in data]
    
    if (table_name in ("news", "categories", "contents", "tags")):
        time_col = {"load_dt": datetime.now()} if (table_name in ("news", "contents")) else {"update_dt": datetime.now()}
        fmt_row_data = [{**row, **time_col} for row in row_data]
    else:
        fmt_row_data = row_data

    records = [TABLE_MODELS[table_name](**row) for row in fmt_row_data]
    
    db.add_all(records)
    db.commit()


