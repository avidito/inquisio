from datetime import datetime
import os

from settings import *

def get_params():
    """Get parameters value from configuration file"""

    param_names = ["TOPIC", "BOOTSTRAP_SERVER", "TMP_PATH"]

    params = {param: globals().get(param) for param in param_names}
    return params

def logging(message):
    """Print message with time namespace"""

    nmspc = datetime.now().strftime("[%Y-%m-%d %H:%M:%d]")
    print(f"{nmspc} {message}")
