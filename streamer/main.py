from utils import get_prompt, get_params, create_job_report, export_report
from producer import get_producer
from scraper import run_scraper

########## MAIN ##########
if __name__ == "__main__":
    prompt_params = get_prompt()
    [scraper_params, producer_params] = get_params()

    producer = get_producer(producer_params)
    report_data = run_scraper(producer, scraper_params, prompt_params)
    report = create_job_report(report_data, prompt_params)

    export_report(report)
    print(report)
