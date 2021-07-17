from datetime import datetime

# Import list of scraper runner
from .job.okezone import scraper as okezone_scraper
from .job.sindonews import scraper as sindonews_scraper
from .job.detik import scraper as detik_scraper
from .job.kompas import scraper as kompas_scraper

# Scraper runner wrapper
def run_all_categories(scraper, meta):
    def wrapper(delay, dt, producer):
        website_report = []
        for category, url in meta:
            report = scraper(category, url, delay, dt, producer)
            website_report.append(report)
        return website_report
    return wrapper

# Scraper map
scraper_func = {
    "okezone": okezone_scraper,
    "sindonews": sindonews_scraper,
    "detik": detik_scraper,
    "kompas": kompas_scraper
}

# Run all scrapper batch runner
def run_scraper(producer, scraper_params, prompt_params):
    meta = scraper_params["SCRAPER_META"]
    delay = scraper_params["DELAY"]
    dt = prompt_params["DATE"]
    all_reports = {}

    # Start scraper job
    start_dt = datetime.now()
    for scraper in meta.keys():
        run_batch_scraper = run_all_categories(scraper_func[scraper], meta[scraper])
        all_reports[scraper] = run_batch_scraper(delay, dt, producer)
    end_dt = datetime.now()
    return {"start_dt": start_dt, "end_dt": end_dt, **all_reports}
