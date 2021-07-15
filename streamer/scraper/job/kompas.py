import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

from . import Logger, reformat_dt, cvt_ts, export_news

###### Navigation ######
def navigate_page(url, delay, log, query=None, path=None, data=None):
    """Navigate to new page"""

    # Get page html
    req = requests.get(url, params=query)
    log.log_navigation(req.url, req.status_code, delay)
    time.sleep(delay)
    return req.url, BeautifulSoup(req.content, "lxml")

###### Extraction ######
def extract_all_news(producer, log, page, delay):
    """Extract all news provided in current page"""

    news_list = page.find_all("div", attrs={"class": "article__list"})
    cnt = 0
    for news in news_list:
        extract_news(news, delay, log)
        cnt += 1
    return cnt

def extract_news(news, delay, log):
    """Extract information from single news"""

    title = news.find("h3", attrs={"class": "article__title"}).text
    category = news.find("div", attrs={"class": "article__subtitle"}).text
    url = news.find("a", attrs={"class": "article__link"}).get("href")
    post_dt = cvt_ts(news.find("div", attrs={"class": "article__date"}).text)

    info = extract_news_content(url, delay, log)

    news_data = {"title": title, "category": category, "author": info["author"], "post_dt": post_dt, "tags": info["tags"], "content": info["content"], "url": url}
    export_news(news_data)

def extract_news_content(url, delay, log):
    """Extracting more detail information from news article page"""

    params = {"page": "all"}

    [current_url, news_html] = navigate_page(url, delay, log, params)

    # Author
    author_block = news_html.find("div", attrs={"id": "penulis"})
    if (author_block):
        author = author_block.text
        author_clr = author.split("Penulis")[1]
    else:
        author = news_html.find("div", attrs={"id": "editor"}).text
        author_clr = author.split("Editor")[1]

    # Tags
    tags = [tag.text for tag in news_html.find_all("a", attrs={"class": "tag__article__link"})]

    # Content
    content = None #extract_paginate_content(news_html, delay, log)

    return {"author": author_clr, "tags": tags, "content": content}

def extract_paginate_content(page, delay, log):
    """Extract news content"""

    content = [p.text for p in page.find("div", attrs={"class": "read__content"}).find_all("p")]

    return " ".join(content)

###### Get Element ######
def get_next_index_page_url(page):
    """Get next page url from next button"""

    next_button = page.find("a", attrs={"class": "paging__link"}, string="Next")
    next_url = next_button.get("href") if (next_button) else None
    return next_url

###### Main ######
def scraper(category, url, delay, dt, producer):
    log = Logger("kompas", category, delay=delay, url=url)
    all_news_cnt = 0

    params = {"date": dt}

    # Go to initial point
    log.log_start()
    [current_url, page_html] = navigate_page(url, delay, log, params)

    while(1):
        cnt = extract_all_news(producer, log, page_html, delay)
        log.add_news_count(cnt)

        next_url = get_next_index_page_url(page_html)
        if (next_url):
            [current_url, page_html] = navigate_page(next_url, delay, log)
        else:
            break

    log.log_finish()
