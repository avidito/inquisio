from settings import *

def get_params():
    """Get parameters value from configuration file"""

    scraper_params = ["DELAY", "SCRAPER_META"]
    producer_params = ["TOPIC", "BOOTSTRAP_SERVER"]

    scraper = {param: globals().get(param) for param in scraper_params}
    producer = {param: globals().get(param) for param in producer_params}
    return scraper, producer


########## Job Reporting ##########
def create_job_report(report_data):
    """Create job report"""
    border = "#" * 50
    header = "Scraper Job Report"
    report = "\n\n".join([
        border,
        header,
        gen_rpt_execution_details(report_data),
        gen_rpt_params_report(report_data),
        gen_rpt_scraper_result(report_data),
        border
    ])
    return report

def gen_rpt_execution_details(report_data):
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

def gen_rpt_params_report(report_data):
    """Generate formatted params from job result data"""

    # Format data
    header = "--- Params ---"
    param_list = "\n".join([f"> {name} = {value}" for name, value in [("job_date", "2021-07-13")]])

    # Assemble data
    params = "\n".join([
        header, param_list
    ])
    return params

def gen_rpt_scraper_result(report_data):
    """Generate formatted scaper result from job result data"""

    # Format data
    header = "--- Scraper Result ---"
    scraper_list = "\n\n".join([gen_rpt_scraper_info(*scraper_meta) for scraper_meta in report_data.items()])

    # Assemble data
    scraper_result = "\n".join([
        header, scraper_list
    ])
    return scraper_result

def gen_rpt_scraper_info(website, meta):
    """Generate formatted single scraper info from job result data"""

    # Format data
    website = f"> {website}"
    execution_time    = f"    execution_time        : ?? seconds"
    news_scraped      = f"    news_scraped          : ?? news"
    category_news_cnt = f"    category (news_count) :\n" + "\n".join([f"        - {info['category']} ({info['total_news']})" for info in meta])

    # Assemble data
    scraper_info = "\n".join([
        website, execution_time, news_scraped, category_news_cnt
    ])
    return scraper_info

def export_report(report):
    """Export report to txt file"""
    with open("report.txt", "w+", encoding="utf-8") as file:
        file.write(report)
