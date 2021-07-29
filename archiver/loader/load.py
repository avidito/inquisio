import csv
from datetime import datetime

from database.engine import session_factory
from database.models import TABLE_MODELS
from utils import remove_duplicate, log_db_process

##### MAIN #####
def load_data_to_db(tmp, table_list, db_session):
    """Loading processed data to table"""

    for table_name, pk in table_list.items():
        header, data = read_data(table_name, tmp=tmp)
        data = remove_duplicate(data, header, pk)

        truncate_table(table_name, db_session=db_session)
        load_data(table_name, db_session=db_session, header=header, data=data)

##### CRUD #####
@log_db_process
def read_data(table_name, tmp):
    """Read data from csv file"""

    path = f"{tmp}/prc_{table_name}.csv"
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")
        header, *data = reader
    return header, data

@log_db_process
def truncate_table(table_name, db_session):
    """Truncate database table"""

    table = TABLE_MODELS[table_name]
    with db_session() as db:
        db.query(table).delete()

@log_db_process
def load_data(table_name, db_session, header, data):
    """Load data to table"""

    row_data = [{col: value for col, value in zip(header, row)} for row in data]

    # Add time data
    if (table_name in ("news", "categories", "contents", "tags")):
        time_col = {"load_dt": datetime.now()} if (table_name in ("news", "contents")) else {"update_dt": datetime.now()}
        fmt_row_data = [{**row, **time_col} for row in row_data]
    else:
        fmt_row_data = row_data

    records = [TABLE_MODELS[table_name](**row) for row in fmt_row_data]
    with db_session() as db:
        db.add_all(records)
