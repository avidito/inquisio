from settings import *

def get_params():
    """Get parameters value from configuration file"""

    scraper_params = ["DELAY", "SCRAPER_META"]
    producer_params = ["TOPIC", "BOOTSTRAP_SERVER"]

    scraper = {param: globals().get(param) for param in scraper_params}
    producer = {param: globals().get(param) for param in producer_params}
    return scraper, producer


########## Job Reporting ##########
def create_job_report():
    """Create job report"""
    header = "Scraper Job Report"
    report = "\n\n".join([
        header, gen_rpt_execution_details(), gen_rpt_params_report(), gen_rpt_scraper_result()
    ])
    return report

def gen_rpt_execution_details():
    """Generate formatted execution details from job result data"""

    # Format data
    header = "--- Execution Details ---"
    start_time     = "Start Time     : 2021-07-01 10:30:15"
    end_time       = "Finish Time    : 2021-07-01 12:48:12"
    execution_time = "Execution Time : 2 hour 17 minutes 57 seconds"
    total_news     = "Total News     : 173"
    active_scraper = "Active Scraper :\n" + "\n".join(["    - detik", "    - kompas"])

    # Assemble data
    execution_details = "\n".join([
        header, start_time, end_time, execution_time, total_news, active_scraper
    ])
    return execution_details

def gen_rpt_params_report():
    """Generate formatted params from job result data"""

    # Format data
    header = "--- Params ---"
    param_list = "\n".join([f"> {name} = {value}" for name, value in [("job_date", "2021-07-13")]])

    # Assemble data
    params = "\n".join([
        header, param_list
    ])
    return params

def gen_rpt_scraper_result():
    """Generate formatted scaper result from job result data"""

    # Format data
    header = "--- Scraper Result ---"
    scraper_list = "\n\n".join([gen_rpt_scraper_info(*scraper_meta) for scraper_meta in [("detik", "meta")]])

    # Assemble data
    scraper_result = "\n".join([
        header, scraper_list
    ])
    return scraper_result

def gen_rpt_scraper_info(website, meta):
    """Generate formatted single scraper info from job result data"""

    # Format data
    website = "> detik"
    execution_time    = "    execution_time        : 40 minutes 23 seconds"
    news_scraped      = "    news_scraped          : 60 news"
    category_news_cnt = "    category (news_count) :\n" + "\n".join([f"        - {ctg} ({cnt})" for ctg, cnt in [("news", 30), ("finance", 12)]])

    # Assemble data
    scraper_info = "\n".join([
        website, execution_time, news_scraped, category_news_cnt
    ])
    return scraper_info
