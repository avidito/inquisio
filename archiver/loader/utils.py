from datetime import datetime, timedelta
import os
import json

from settings import *

def logging(message):
    """Print message with time namespace"""

    nmspc = datetime.now().strftime("[%Y-%m-%d %H:%M:%d]")
    print(f"{nmspc} {message}")

def get_params():
    """Get parameters value from configuration file"""

    param_names = ["TMP_PATH", "DMP_PATH", "TABLE_LIST"]

    params = {param: globals().get(param) for param in param_names}
    return params

def get_data(path, offset=0):
    """Get data with offset days from tmp folder"""

    day_dt = datetime.now() + timedelta(days=offset)
    try:
        day_path = os.path.join(path, f"{day_dt.strftime('%Y%m%d')}_result.json")
        with open(day_path, "r", encoding="utf-8") as file:
            data = [json.loads(row) for row in file]
    except FileNotFoundError:
        data = []

    return data

def check_dir_path(path):
    """Check dump folder existence and create if the folder is not exist"""

    if (os.path.exists(path)):
        return True

    os.mkdir(path)

def export_report():
    ...