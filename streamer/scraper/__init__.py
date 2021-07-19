from datetime import datetime

# Import list of scraper runner
from .job.okezone import scraper as okezone_scraper
from .job.sindonews import scraper as sindonews_scraper
from .job.detik import scraper as detik_scraper
from .job.kompas import scraper as kompas_scraper

# Print start log
def start_log(start_dt, prompt_params):
    nmspc = start_dt.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{nmspc} Starting scraper with following params:")
    print(f"{' ' * 21} {prompt_params}")

# Print end log
def end_log(end_dt):
    nmspc = end_dt.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{nmspc} Finishing scraper. Check report for job details")

# Scraper runner wrapper
def run_all_categories(scraper, meta, excluded_urls, mode):
    def wrapper(delay, dt, producer):
        website_report = []
        for category, url in meta:
            ex_url = excluded_urls.get(category, []) if (excluded_urls) else []
            report = scraper(category, url, delay, dt, ex_url, producer, mode)
            website_report.append(report)
        return website_report
    return wrapper

# Scraper map
scraper_func = {
    "detik": detik_scraper,
    "kompas": kompas_scraper,
    "okezone": okezone_scraper,
    "sindonews": sindonews_scraper,
}

# Run all scrapper batch runner
def run_scraper(producer, scraper_params, prompt_params):
    meta = scraper_params["SCRAPER_META"]
    delay = scraper_params["DELAY"]
    excluded_urls = scraper_params["EXCLUDED_URLS"]
    dt = prompt_params["DATE"]
    mode = prompt_params["MODE"]
    all_reports = {}

    # In debug mode, initiate empty result.json file
    if(mode == "debug"):
        with open("result.json", "w+", encoding="utf-8") as file:
            pass

    # Start scraper job
    start_dt = datetime.now()
    start_log(start_dt, prompt_params)
    for scraper in meta.keys():
        if (meta[scraper]): # Scrape only website with assigned category and url
            run_batch_scraper = run_all_categories(scraper_func[scraper], meta[scraper], excluded_urls.get(scraper), mode)
            all_reports[scraper] = run_batch_scraper(delay, dt, producer)
    end_dt = datetime.now()
    end_log(end_dt)
    return {"start_dt": start_dt, "end_dt": end_dt, **all_reports}
