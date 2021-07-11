import requests
import time
from bs4 import BeautifulSoup

from . import Logger, reformat_dt, cvt_ts, split_date, export_news

###### Navigation ######
def navigate_page(url, delay, log, query=None, path=None, data=None):
    """Navigate to new page"""

    # Inject path to url
    url_fin = url
    if (data):
        [year, month, day] = split_date(data["date"])
        data = {"thn": year, "bln": month, "tgl": day}

    # Get page html
    req = requests.post(url_fin, data=data, allow_redirects=True) if (data) else requests.get(url_fin)
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
    content = extract_paginate_content(news_html, delay, log)

    return {"author": author, "tags": tags, "content": fmt_content(content)}

def extract_paginate_content(page, delay, log):
    """Extracting news content from all pagination in the article"""
    content = []
    current_page = page
    while(1):
        current_page_content = current_page.find("div", attrs={"id": "contentx"}).find_all("p")
        content.extend(current_page_content)

        next_url = get_next_news_page_url(current_page)
        if (next_url):
            [current_url, current_page] = navigate_page(next_url, delay, log)
        else:
            break

    return content

###### Get Element ######
def get_next_index_page_url(page):
    """Get next page url from next button"""

    next_button = page.find("a", attrs={"rel": "next"})
    next_url = next_button["href"] if (next_button) else None
    return next_url

def get_next_news_page_url(page):
    """Get next page url from next button"""

    next_url = None
    next_button = page.find("div", attrs={"class": "next"})
    if (next_button):
        next_button = next_button.find("span", text="Selanjutnya")
        next_url = next_button.parent["href"] if (next_button) else None
        next_url = next_url if (next_url != "#") else None
    return next_url

##### Format Element #####
def fmt_content(contents):
    """Format content and remove non-content paragraph blocks"""
    clr = [
        content.text for content in contents
        if ("baca juga" not in content.text.lower()) \
        and ("lihat juga" not in content.text.lower()) \
        and ("saksikan" not in content.text.lower())
    ]
    fmt = ' '.join(clr)
    return fmt

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

        next_url = get_next_index_page_url(page_html)
        if (next_url):
            [current_url, page_html] = navigate_page(next_url, delay, log)
        else:
            break

    log.log_finish()
