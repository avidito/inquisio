# Import list of scraper runner
from .job.okezone import scraper as okezone_scraper
from .job.sindonews import scraper as sindonews_scraper
from .job.detik import scraper as detik_scraper
from .job.kompas import scraper as kompas_scraper

# Scraper runner wrapper
def run_all_categories(scraper, meta):
    def wrapper(delay, dt, producer):
        for category, url in meta:
            scraper(category, url, delay, dt, producer)
    return wrapper

# Scraper map
scraper_func = {
    "okezone": okezone_scraper,
    "sindonews": sindonews_scraper,
    "detik": detik_scraper,
    "kompas": kompas_scraper
}

# Run all scrapper batch runner
def run_scraper(producer, params, dt):
    meta = params["SCRAPER_META"]
    delay = params["DELAY"]
    for scraper in meta.keys():
        run_batch_scraper = run_all_categories(scraper_func[scraper], meta[scraper])
        run_batch_scraper(delay, dt, producer)
