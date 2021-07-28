import csv

from engine import get_engine
from models import TABLE_MODELS


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
    row_data = []
    for row in data:
        row_data.extend([{col: value for col, value in zip(header, row)}])
    records = [TABLE_MODELS[table_name](**row) for row in row_data]
    
    db.add_all(records)
    db.commit()


TMP = "__tmp"
TABLE_LIST = ["map_news_tags"]

db = get_engine()

for table_name in TABLE_LIST:
    header, data = read_data(table_name, TMP)
    truncate_table(db, table_name)
    load_data(db, table_name, header, data)
