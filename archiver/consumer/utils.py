from datetime import datetime
import os

from settings import *

def logging(message):
    """Print message with time namespace"""

    nmspc = datetime.now().strftime("[%Y-%m-%d %H:%M:%d]")
    print(f"{nmspc} {message}")

def get_params():
    """Get parameters value from configuration file"""

    param_names = ["TOPIC", "BOOTSTRAP_SERVER", "DMP_PATH"]

    params = {param: globals().get(param) for param in param_names}
    return params

def check_dir_path(path):
    """Check folder existence and create if the folder is not exist"""

    if (os.path.exists(path)):
        return True

    os.makedir(path)

def export_data(data, path):
    """Exporting data to tmp folder based on received date"""

    check_dir_path(path)
    today_dt = datetime.now().strftime("%Y%d%m")
    data_path = os.path.join(path, f"{today_dt}_results.json")
    with open(data_path, "a+", encoding="UTF-8") as file:
        file.write(f"{data.value}\n")
