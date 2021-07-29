from datetime import datetime, timedelta
import os
import json

from settings import *

##### Log #####
def logging(message):
    """Print message with time namespace"""

    nmspc = datetime.now().strftime("[%Y-%m-%d %H:%M:%d]")
    print(f"{nmspc} {message}")

def log_process(func):
    """Logging wrapper to add time data"""

    def wrapper(*data):
        time_namespace = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        message = f"Running `{func.__name__}` process"
        print(f"{time_namespace} {message}")
        result = func(*data)
        return result
    return wrapper

def log_db_process(func):
    """Logging wrapper to add time data"""

    def wrapper(table_name, **params):
        time_namespace = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        message = f"Executing `{func.__name__}` process for `{table_name}`"
        print(f"{time_namespace} {message}")
        result = func(table_name, **params)
        return result
    return wrapper

##### Params #####
def get_params():
    """Get parameters value from configuration file"""

    dir_params = ["TMP_PATH", "DMP_PATH", "SQL_PATH"]
    db_params = ["TABLE_LIST", "MAP_CATEGORIES", "USERNAME", "PASSWORD", "HOSTNAME", "PORT", "DATABASE"]

    dir = {param: globals().get(param) for param in dir_params}
    db = {param: globals().get(param) for param in db_params}
    return dir, db

def check_dir_path(path):
    """Check dump folder existence and create if the folder is not exist"""

    if (os.path.exists(path)):
        return True

    os.mkdir(path)

##### Data #####
def get_data(path, offset=0):
    """Get data with offset days from tmp folder"""

    day_dt = datetime.now() + timedelta(days=offset)
    try:
        day_path = os.path.join(path, f"{day_dt.strftime('%Y%m%d')}_results.json")
        with open(day_path, "r", encoding="utf-8") as file:
            data = [json.loads(row) for row in file]
    except FileNotFoundError:
        data = []

    return data

def remove_duplicate(data, header, pk):
    """Removing duplicate data based on its table primary key"""

    check = set()
    pk_id = [header.index(key) for key in pk]
    cln_data = []
    for row in data:
        row_pk_value = tuple(row[i] for i in pk_id)
        if (row_pk_value in check):
            continue
        else:
            cln_data.append(row)
            check.add(row_pk_value)
    return cln_data
