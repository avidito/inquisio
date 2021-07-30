from application.settings import *

def get_params():
    """Get parameters value from configuration file"""

    param_names = ["USERNAME", "PASSWORD", "HOSTNAME", "PORT", "DATABASE"]

    params = {param: globals().get(param) for param in param_names}
    return params
