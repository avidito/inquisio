import sys
from settings import *

def get_prompt():
    """Get prompted parameters when running scraper job"""

    key = ["DATE"]
    prompt = {key: value for key, value in zip(key, sys.argv[1:])}
    return prompt

def get_params():
    """Get parameters value from configuration file"""

    scraper_params = ["DELAY", "SCRAPER_META", "EXCLUDED_URLS"]
    producer_params = ["TOPIC", "BOOTSTRAP_SERVER"]

    scraper = {param: globals().get(param) for param in scraper_params}
    producer = {param: globals().get(param) for param in producer_params}
    return scraper, producer

def create_job_report(report_data, prompt_params):
    """Create job report"""

    border = "#" * 50
    header = "Scraper Job Report"
    report = "\n\n".join([
        border,
        header,
        gen_rpt_execution_details(report_data),
        gen_rpt_params_report(prompt_params),
        gen_rpt_scraper_result(report_data),
        border
    ])
    return report

def export_report(report):
    """Export report to txt file"""

    with open("report.txt", "w+", encoding="utf-8") as file:
        file.write(report)

########## Job Reporting ##########
def gen_rpt_execution_details(report_data):
    """Generate formatted execution details from job result data"""

    # Extract time attribute
    [start_tm, end_tm, exec_tm] = extract_time_attr(report_data)
    [cnt, scraper_list] = extract_job_meta(report_data)

    # Format data
    header = "--- Execution Details ---"
    start_time     = f"Start Time     : {start_tm}"
    end_time       = f"Finish Time    : {end_tm}"
    execution_time = f"Execution Time : {exec_tm}"
    total_news     = f"Total News     : {cnt}"
    active_scraper = f"Active Scraper :\n" \
                   + "\n".join(scraper_list)

    # Assemble data
    execution_details = "\n".join([
        header, start_time, end_time, execution_time, total_news, active_scraper
    ])
    return execution_details

def gen_rpt_params_report(prompt_params):
    """Generate formatted params from job result data"""

    # Format data
    header = "--- Params ---"
    param_list = "\n".join([f"> {name} = {value}" for name, value in prompt_params.items()])

    # Assemble data
    params = "\n".join([
        header, param_list
    ])
    return params

def gen_rpt_scraper_result(report_data):
    """Generate formatted scaper result from job result data"""

    # Format data
    header = "--- Scraper Result ---"
    scraper_list = "\n\n".join([
        gen_rpt_scraper_info(key, value) for key, value in report_data.items() \
        if key not in ("start_dt", "end_dt")
    ])

    # Assemble data
    scraper_result = "\n".join([
        header, scraper_list
    ])
    return scraper_result

def gen_rpt_scraper_info(website, meta):
    """Generate formatted single scraper info from job result data"""
    # Calculate report value
    total_time, total_news, ctg_cnt = extract_scraper_meta(meta)
    spc = " " * 4
    dbl_spc = spc * 2

    # Format data
    website = f"> {website}"
    execution_time      = f"{spc}execution_time        : {convert_seconds_timeformat(total_time)}"
    news_scraped        = f"{spc}news_scraped          : {total_news} news"
    category_news_count = f"{spc}category (news_count) :\n" \
                        + "\n".join([f"{dbl_spc}- {ctg} ({cnt})" for ctg, cnt in ctg_cnt])

    # Assemble data
    scraper_info = "\n".join([
        website, execution_time, news_scraped, category_news_count
    ])
    return scraper_info

########## Report Operations ##########
def extract_scraper_meta(meta):
    """Extract scraper result meta"""

    total_time = 0
    total_news = 0
    ctg_cnt = []
    for info in meta:
        total_time += info["duration"]
        total_news += info["total_news"]
        ctg_cnt.append((info["category"], info["total_news"]))

    return total_time, total_news, ctg_cnt

def convert_seconds_timeformat(total_time=0):
    """Convert string to hour, minutes, seconds format"""

    # Extract time counts
    remainder = total_time
    time_cnt = {}

    time_cnt["hour"] = remainder // 3600
    remainder %= 3600

    time_cnt["minute"] = remainder // 60
    remainder %= 60

    time_cnt["second"] = remainder

    # Create string format
    fmt = ""
    for tm, cnt in time_cnt.items():
        if (cnt):
            fmt += f" {cnt} {tm}" if (cnt == 1) else f" {cnt} {tm}s"
        elif (tm == "second" and fmt == ""):
            fmt += f"0 {tm}"
    return fmt.lstrip()

def extract_time_attr(report_data):
    """Extracting time information from report data"""

    start_tm = report_data["start_dt"].strftime("%Y-%m-%d %H:%M:%S")
    end_tm = report_data["end_dt"].strftime("%Y-%m-%d %H:%M:%S")
    exec_tm = str(int((report_data["end_dt"] - report_data["start_dt"]).total_seconds()))

    return start_tm, end_tm, exec_tm

def extract_job_meta(report_data):
    """Extracting job metadata from report data"""

    cnt = 0
    scraper_list = []
    for key, value in report_data.items():
        if key not in ("start_dt", "end_dt"):
            cnt += sum([info["total_news"] for info in value])
            scraper_list.append(key)
    return cnt, scraper_list
