from datetime import datetime
import json

# Initiate job variable
def init_job(website, topic):
    return datetime.now()

# Return report for job
def finish_job(WEBSITE, CATEGORY, start_dt):
    end_dt = datetime.now()
    duration = (end_dt - start_dt).total_seconds()
    return duration

# Logging wrapper to add time data
def logging(message, **kwargs):
    time_namespace = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{time_namespace} {message}", **kwargs)

# Export file to tmp data
def export_news(list_data):
    result_path = "result.json"
    with open(result_path, "a+", encoding="utf-8", newline="") as file:
        file.write(json.dumps(list_data))
        file.write("\n")
