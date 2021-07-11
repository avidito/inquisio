import requests
import time
from bs4 import BeautifulSoup

from . import Logger, reformat_dt, cvt_ts, export_news

###### Navigation ######
def navigate_page(url, delay, log, query=None, path=None):
    """Navigate to new page"""

    # Inject path to url
    url_fin = url
    if (path):
        path["date"] = reformat_dt(path["date"], from_fmt="%Y-%m-%d", to_fmt="%Y/%m/%d")
        url_fin = requests.compat.urljoin(url_fin, path["date"])

    # Get page html
    req = requests.get(url_fin)
    log.log_navigation(req.url, req.status_code, delay)
    time.sleep(delay)
    return req.url, BeautifulSoup(req.content, "lxml")

###### Extraction ######
def extract_all_news(producer, log, page, delay):
    """Extract all news provided in current page"""

    news_list = page.find("div", attrs={"class": "news-content"}).find_all("li")
    cnt = 0
    for news in news_list:
        extract_news(news, delay, log)
        cnt += 1
    return cnt

def extract_news(news, delay, log):
    """Extract information from single news"""

    title = news.find("h4", attrs={"class": "f17"}).text
    category = news.find("span", attrs={"class": "c-news"}).a.text
    url = news.find("h4", attrs={"class": "f17"}).a.get("href")
    post_dt = str(news.find("time", attrs={"class": "category-hardnews"}).span.next_sibling.string)

    info = extract_news_content(url, delay, log)

    news_data = {"title": title, "category": category, "author": info["author"], "post_dt": cvt_ts(post_dt), "tags": info["tags"], "content": info["content"], "url": url}
    export_news(news_data)

def extract_news_content(url, delay, log):
    """Extracting more detail information from news article page"""

    [current_url, news_html] = navigate_page(url, delay, log)
    author = news_html.find("div", attrs={"class": "namerep"}).find(text=True)
    tags = [tag.text for tag in news_html.find("div", attrs={"class": "newtag"}).find_all("li")]
    content = None

    return {"author": author, "tags": tags, "content": content}

###### Get Element ######
def get_next_page_url(page):
    """ Get next page url from next button """

    next_button = page.find("a", attrs={"rel": "next"})
    next_url = next_button["href"] if (next_button) else None
    return next_url

###### Main ######
def scraper(category, url, delay, dt, producer):
    log = Logger("okezone", category, delay=delay, url=url)
    all_news_cnt = 0

    # Go to initial point
    log.log_start()
    [current_url, page_html] = navigate_page(url, delay, log, path={"date": dt})

    while(1):
        cnt = extract_all_news(producer, log, page_html, delay)
        log.add_news_count(cnt)

        next_url = get_next_page_url(page_html)
        if (next_url):
            [current_url, page_html] = navigate_page(next_url, delay, log)
        else:
            break

    log.log_finish()
