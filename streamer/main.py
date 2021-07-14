from utils import get_params
from producer import get_producer
from scraper import run_scraper, create_job_report

########## MAIN ##########
if __name__ == "__main__":
    [scraper_params, producer_params] = get_params()

    producer = get_producer(producer_params)
    report_data = run_scraper(producer, scraper_params, "2021-07-03")
    report = create_job_report(report_data)
    print(report)
