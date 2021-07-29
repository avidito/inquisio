import csv
from datetime import datetime

from .engine import session_factory
from .models import TABLE_MODELS

##### MAIN #####
def load_data_to_db(params):
    tmp = params["TMP_PATH"]
    table_list = params["TABLE_LIST"]
    username = params["USERNAME"]
    password = params["PASSWORD"]
    hostname = params["HOSTNAME"]
    port = params["PORT"]
    database = params["DATABASE"]

    get_db = session_factory(username, password, hostname, port, database)
    for table_name in table_list:
        header, data = read_data(table_name, tmp)
        truncate_table(get_db, table_name)
        load_data(get_db, table_name, header, data)

##### CRUD #####
def read_data(table_name, tmp):
    path = f"{tmp}/prc_{table_name}.csv"
    with open(path, "r") as file:
        reader = csv.reader(file, delimiter=",")
        header, *data = reader
    return header, data

def truncate_table(get_db, table_name):
    print(f"Truncating table {table_name}")

    table = TABLE_MODELS[table_name]
    with get_db() as db:
        db.query(table).delete()

def load_data(get_db, table_name, header, data):
    print(f"Loading data to table {table_name}")
    row_data = [{col: value for col, value in zip(header, row)} for row in data]

    if (table_name in ("news", "categories", "contents", "tags")):
        time_col = {"load_dt": datetime.now()} if (table_name in ("news", "contents")) else {"update_dt": datetime.now()}
        fmt_row_data = [{**row, **time_col} for row in row_data]
    else:
        fmt_row_data = row_data

    records = [TABLE_MODELS[table_name](**row) for row in fmt_row_data]

    with get_db() as db:
        db.add_all(records)
