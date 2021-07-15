# Import list of scraper runner
from .job.okezone import scraper as okezone_scraper
from .job.sindonews import scraper as sindonews_scraper

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
    "sindonews": sindonews_scraper
}

# Run all scrapper batch runner
def run_scraper(producer, params, dt):
    meta = params["SCRAPER_META"]
    delay = params["DELAY"]
    all_reports = {}

    for scraper in meta.keys():
        run_batch_scraper = run_all_categories(scraper_func[scraper], meta[scraper])
        all_reports[scraper] = run_batch_scraper(delay, dt, producer)

    return all_reports
