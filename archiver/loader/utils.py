from settings import *

def logging(message):
    """Print message with time namespace"""

    nmspc = datetime.now().strftime("[%Y-%m-%d %H:%M:%d]")
    print(f"{nmspc} {message}")

def get_params():
    """Get parameters value from configuration file"""

    param_names = ["TMP_PATH"]

    params = {param: globals().get(param) for param in param_names}
    return params

def get_data():
    ...

def export_data():
    ...
