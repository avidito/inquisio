from settings import *

# Get parameters value from configuration file
def get_params():
    scraper_params = ["DELAY", "SCRAPER_META"]
    producer_params = ["TOPIC", "BOOTSTRAP_SERVER"]

    scraper = {param: globals().get(param) for param in scraper_params}
    producer = {param: globals().get(param) for param in producer_params}
    return scraper, producer
