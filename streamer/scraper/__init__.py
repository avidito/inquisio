# Import list of scraper runner
from .job.okezone import scraper as okezone_scraper

# Scraper runner wrapper
def run_all_categories(scraper, meta):
    def wrapper(delay, dt, producer):
        for category, url in meta:
            scraper(category, url, delay, dt, producer)
    return wrapper

# Scraper map
scraper_func = {
    "okezone": okezone_scraper
}

# Run all scrapper batch runner
def run_scraper(producer, params, dt):
    meta = params["SCRAPER_META"]
    delay = params["DELAY"]
    for scraper in scraper_func.keys():
        run_batch_scraper = run_all_categories(scraper_func[scraper], meta[scraper])
        run_batch_scraper(delay, dt, producer)
