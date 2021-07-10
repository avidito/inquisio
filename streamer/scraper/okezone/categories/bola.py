import requests
from bs4 import BeautifulSoup
import time
import dateparser

from _utils import init_job, finish_job, logging, export_news

URL = "https://bola.okezone.com/indeks/"
DELAY = 10
WEBSITE = "okezone"
CATEGORY = "bola"

# Navigate to new page with date parameters
def navigate_page(url, date, delay):
    params = {"date": date.strftime("%Y/%m/%d")} if (date) else None
    logging(f"Requesting : {url} with params: {params}")

    inj_url = requests.compat.urljoin(url, (params.get("date") if (params) else None))
    req = requests.get(inj_url)
    logging(f"Status : {req.status_code}. Sleep for {delay} second(s)")
    time.sleep(delay)

    return req.url, BeautifulSoup(req.content, "lxml")

# Extract all news information from a page
def extract_all_news(page, delay):
    logging("Extracting all news information on pages")
    news_list = page.find("div", attrs={"class": "news-content"}).find_all("li")
    news_info = [
        extract_news(news, delay) for news in news_list
    ]
    return news_info, len(news_info)

# Extract information from single news
def extract_news(news, delay):
    title = news.find("h4", attrs={"class": "f17"}).text
    category = news.find("span", attrs={"class": "c-news"}).a.text
    url = news.find("h4", attrs={"class": "f17"}).a.get("href")

    # Get author, tags, and content
    info = extract_news_info(url, delay)

    # Convert time data to UNIX timestamp
    post_dt = str(news.find("time", attrs={"class": "category-hardnews"}).span.next_sibling.string)
    post_dt = int(dateparser.parse(post_dt.replace("'", "").replace("Minggu", "Ahad"), languages=["id"]).timestamp())

    return {"title": title, "category": category, "author": info["author"], "post_dt": post_dt, "tags": info["tags"], "content": info["content"], "url": url}

# Navigate to news page
def navigate_news_page(url, delay):
    logging(f"Extracting information from {url}")
    req = requests.get(url)
    logging(f"Status : {req.status_code}. Sleep for {delay} second(s)")
    time.sleep(delay)

    return req.url, BeautifulSoup(req.content, "lxml")

# Extracting information from news page
def extract_news_info(url, delay):
    [current_url, news_html] = navigate_news_page(url, delay)

    author = news_html.find("div", attrs={"class": "namerep"}).find(text=True)
    tags = [tag.text for tag in news_html.find("div", attrs={"class": "newtag"}).find_all("li")]
    content = None

    return {"author": author, "tags": tags, "content": content}

# Get next page link from next button
def get_next_page_url(page):
    next_button = page.find("a", attrs={"rel": "next"})
    next_url = next_button.get("href", None) if (next_button) else None
    return next_url


########## MAIN ##########
if __name__ == "__main__":
    start_dt = init_job(WEBSITE, CATEGORY)
    all_news_cnt = 0

    # Starting extraction
    logging(f"Starting web-scraping process for {WEBSITE} - {CATEGORY}")
    [current_url, page_html] = navigate_page(URL, start_dt, DELAY)

    while(1):
        # Extract information
        [news_cp_info, news_cp_cnt] = extract_all_news(page_html, DELAY)
        export_news(news_cp_info)
        all_news_cnt += news_cp_cnt

        # Get next page url
        next_url = get_next_page_url(page_html)
        if (next_url):
            [current_url, page_html] = navigate_page(next_url, None, DELAY)
        else:
            break

    duration = finish_job(WEBSITE, CATEGORY, start_dt)
    logging(f"Finishing web-scraping process for {WEBSITE} - {CATEGORY}. Total execution time: {duration} second(s), Total extracted info: {all_news_cnt}")
