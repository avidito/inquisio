import requests
import time
from bs4 import BeautifulSoup

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

    news_list = page.find("div", attrs={"class": "indeks-news"}).find_all("div", attrs={"class": "indeks-rows"})
    cnt = 0
    for news in news_list:
        extract_news(news, delay, log)
        cnt += 1
    return cnt

def extract_news(news, delay, log):
    """Extract information from single news"""

    title = news.find("div", attrs={"class": "indeks-title"}).text
    category = news.find("div", attrs={"class": "mini-info"}).find("li").text
    url = news.find("div", attrs={"class": "indeks-title"}).a["href"]
    post_dt = cvt_ts(news.find("div", attrs={"class": "mini-info"}).find("p").text)

    info = extract_news_content(url, delay, log)

    news_data = {"title": title, "category": category, "author": info["author"], "post_dt": post_dt, "tags": info["tags"], "content": info["content"], "url": url}
    export_news(news_data)

def extract_news_content(url, delay, log):
    """Extracting more detail information from news article page"""

    [current_url, news_html] = navigate_page(url, delay, log)

    author = news_html.find("a", attrs={"rel": "author"}).text
    tags = [tag.text for tag in news_html.find("div", attrs={"class": "tag-list"}).find_all("li")]
    content = extract_paginate_content(news_html, delay, log)

    return {"author": author, "tags": tags, "content": content}

def extract_paginate_content(page, delay, log):
    """Extract news content"""

    content = []
    current_page = page
    while(1):
        current_page_content = current_page.find("div", {"id": "content"})
        clr_content = ops_clear_nonnews(current_page_content)
        content.append(clr_content)

        next_url = get_next_news_page_url(current_page)
        if (next_url):
            [current_url, current_page] = navigate_page(next_url, delay, log)
        else:
            break

    return " ".join(content)

###### Get Element ######
def get_next_index_page_url(page):
    """Get next page url from next button"""

    next_button = page.find("a", attrs={"rel": "next"})
    next_url = next_button["href"] if (next_button) else None
    return next_url

def get_next_news_page_url(page):
    """Get next page url from next button"""

    next_button = page.find("li", attrs={"class": "article-next"})
    next_url = next_button.a["href"] if (next_button) else None
    return next_url

###### Operations ######
def ops_clear_nonnews(content_blocks):
    content_txt = []
    for block in content_blocks:
        try:
            txt = block.text if (block.name != "div") else ''
        except AttributeError:
            txt = str(block)
        finally:
            content_txt.append(txt)

    content_clr = [
        txt for txt in content_txt \
        if (txt != "") \
        and ("baca juga" not in txt)
    ]

    return " ".join(content_clr)

###### Main ######
def scraper(category, url, delay, dt, producer):
    log = Logger("sindonews", category, delay=delay, url=url)
    all_news_cnt = 0

    # Go to initial point
    log.log_start()
    [current_url, page_html] = navigate_page(url, delay, log, query={"t": dt})

    while(1):
        cnt = extract_all_news(producer, log, page_html, delay)
        log.add_news_count(cnt)

        next_url = get_next_index_page_url(page_html)
        if (next_url):
            [current_url, page_html] = navigate_page(next_url, delay, log)
        else:
            break

    log.log_finish()
