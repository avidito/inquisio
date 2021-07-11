from datetime import datetime
import dateparser
import json

class Logger:
    def __init__(self, website, category, **params):
        self.website = website
        self.category = category
        self.params = {**params}
        self.cnt = 0

    def add_news_count(self, cnt):
        """Add news counter"""

        self.cnt += cnt

    def get_datetime_namespace(self):
        """Get current time in datetime and str namespace format"""

        now_dt = datetime.now()
        return now_dt, now_dt.strftime("[%Y-%m-%d %H:%M:%S]")

    def log_start(self):
        """Logging job start"""

        dt_now, dt_nspc = self.get_datetime_namespace()
        print(f"{dt_nspc} Starting scraper for {self.website} - {self.category}. Using parameters: {self.params}")
        self.start_time = dt_now

    def log_navigation(self, url, status_code, delay):
        """Logging page navigation"""

        dt_now, dt_nspc = self.get_datetime_namespace()
        print(f"{dt_nspc} Navigate to page {url}. Status code: {status_code}. Sleep for {delay} second(s)")

    def log_finish(self):
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        print(f"Finishing web-scraping process for {self.website} - {self.category}. Total execution time: {self.duration} second(s). Total extracted info: {self.cnt}")

def reformat_dt(dt, from_fmt, to_fmt):
    """Change datetime format to other format"""

    dt_from = datetime.strptime(dt, from_fmt)
    dt_to = dt_from.strftime(to_fmt)
    return dt_to

def cvt_ts(dt):
    """Convert datetime from string to UNIX timestamp"""

    parsed = dateparser.parse(dt.replace("'", "").replace("Minggu", "Ahad"), languages=["id"])
    return int(parsed.timestamp())

# TEMPORARY
def export_news(news):
    """Export news information to csv"""

    result_path = "result.json"
    with open(result_path, "a+", encoding="utf-8", newline="") as file:
        file.write(json.dumps(news))
        file.write("\n")
