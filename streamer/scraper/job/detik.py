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

    news_list = page.find_all("article", attrs={"class": "list-content__item"})
    cnt = 0
    for news in news_list:
        extract_news(news, delay, log)
        cnt += 1
    return cnt

def extract_news(news, delay, log):
    """Extract information from single news"""

    title = news.find("h3", attrs={"class": "media__title"}).text
    url = news.find("a", attrs={"class": "media__link"}).get("href")
    category = url.split("//")[1].split(".")[0]
    post_dt = news.find("div", attrs={"class": "media__date"}).span.get("d-time")

    info = extract_news_content(url, delay, log)

    news_data = {"title": title, "category": category, "author": info["author"], "post_dt": post_dt, "tags": info["tags"], "content": info["content"], "url": url}
    export_news(news_data)

def extract_news_content(url, delay, log):
    """Extracting more detail information from news article page"""

    params = {"single": "1"}

    [current_url, news_html] = navigate_page(url, delay, log, params)

    # Category
    # category = news_html.find("div", attrs={"class": "page__breadcrumb"}).find_all("a")[-1].text

    # Author
    author = news_html.find("div", attrs={"class": "detail__author"}).text
    author = author.split(" - ")[0]

    # Tags
    tags = [tag.text for tag in news_html.find_all("a", attrs={"class": "nav__item"})]

    content = extract_paginate_content(news_html, delay, log)

    return {"author": author, "tags": tags, "content": content}

def extract_paginate_content(page, delay, log):
    """Extract news content"""

    content = [p.text for p in page.find("div", attrs={"class": "detail__body-text"}).find_all("p")]
    clr_content = ops_clear_nonnews(content)

    return clr_content

###### Get Element ######
def get_next_index_page_url(page):
    """Get next page url from next button"""

    next_button = page.find("a", string="Next")
    next_url = next_button.get("href")
    return next_url
    
###### Operations ######
def ops_clear_nonnews(content_blocks):
    """Clear non-news (e.g., ads, another news link) from content"""

    # content_txt = []
    # for block in content_blocks:
    #     try:
    #         txt = block.text if (block.name != "div") else ''
    #     except AttributeError:
    #         txt = str(block)
    #     finally:
    #         content_txt.append(txt)

    # content_clr = [
    #     txt for txt in content_txt \
    #     if (txt != "") \
    #     and ("baca juga" not in txt)
    # ]

    return " ".join(content_blocks)

###### Main ######
def scraper(category, url, delay, dt, producer):
    log = Logger("detik", category, delay=delay, url=url)
    all_news_cnt = 0

    dt = datetime.strptime(dt, "%Y-%m-%d")
    params = {"date": dt.strftime("%m/%d/%Y")}

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
