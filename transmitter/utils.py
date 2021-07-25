from datetime import datetime
import os

from settings import *

def get_params():
    """Get parameters value from configuration file"""

    sink_params = ["SINK_TOPIC", "SINK_BOOTSTRAP_SERVER"]
    transmitter_params = ["TRANSMITTER_TOPIC", "TRANSMITTER_BOOTSTRAP_SERVER"]

    sink = {param: globals().get(param) for param in sink_params}
    transmitter = {param: globals().get(param) for param in transmitter_params}
    return sink, transmitter

def logging(message):
    """Print message with time namespace"""

    nmspc = datetime.now().strftime("[%Y-%m-%d %H:%M:%d]")
    print(f"{nmspc} {message}")
