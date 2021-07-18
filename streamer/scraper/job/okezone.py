import requests
import time
from bs4 import BeautifulSoup

from . import Logger, reformat_dt, cvt_ts, split_date, check_url
from . import export_news # For testing purpose

###### Navigation ######
def navigate_page(url, delay, log, query=None, path=None, data=None):
    """Navigate to new page"""

    # Prepare POST data
    url_fin = url
    if (query):
        [year, month, day] = split_date(query["date"])
        query = {"thn": year, "bln": month, "tgl": day}

    # Get page html
    req = requests.get(url_fin, params=query)
    log.log_navigation(req.url, req.status_code, delay)
    time.sleep(delay)
    return req.url, BeautifulSoup(req.content, "lxml")

###### Extraction ######
def extract_all_news(producer, log, page, excluded_url, delay):
    """Extract all news provided in current page"""

    news_list = page.find("div", attrs={"class": "news-content"}).find_all("li")
    cnt = 0
    for news in news_list:
        news_data = extract_news(news, delay, excluded_url, log)
        if (news_data):
            producer.publish_data(news_data)
            export_news(news_data) # For testing purpose
            cnt += 1
    return cnt

def extract_news(news, delay, excluded_url, log):
    """Extract information from single news"""

    # Begin Extraction
    title = news.find("h4", attrs={"class": "f17"}).text
    category = news.find("span", attrs={"class": "c-news"}).a.text
    url = news.find("h4", attrs={"class": "f17"}).a.get("href")
    post_dt = cvt_ts(str(news.find("time", attrs={"class": "category-hardnews"}).span.next_sibling.string))

    # If URL is included in excluded_url
    info = extract_news_content(url, excluded_url, delay, log)
    if (info is None):
        return None

    news_data = {"title": title, "category": category, "author": info["author"], "post_dt": post_dt, "tags": info["tags"], "content": info["content"], "url": url}
    return news_data

def extract_news_content(url, excluded_url, delay, log):
    """Extracting more detail information from news article page"""

    [current_url, news_html] = navigate_page(url, delay, log)
    if (not check_url(current_url, excluded_url)):
        return None

    author = news_html.find("div", attrs={"class": "namerep"}).find(text=True)
    tags = [tag.text for tag in news_html.find("div", attrs={"class": "newtag"}).find_all("li")]
    content = extract_paginate_content(news_html, delay, log)

    return {"author": author, "tags": tags, "content": content}

def extract_paginate_content(page, delay, log):
    """Extracting news content from all pagination in the article"""

    content = []
    current_page = page
    while(1):
        current_page_content = current_page.find("div", attrs={"id": "contentx"}).find_all("p")
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

    next_url = None
    next_button = page.find("div", attrs={"class": "next"})
    if (next_button):
        next_button = next_button.find("span", text="Selanjutnya")
        next_url = next_button.parent["href"] if (next_button) else None
        next_url = next_url if (next_url != "#") else None
    return next_url

###### Operations ######
def ops_clear_nonnews(content_blocks):
    """Clear non-news (e.g., ads, another news link) from content"""

    content_clr = [
        content.text for content in content_blocks
        if ("baca juga" not in content.text.lower()) \
        and ("lihat juga" not in content.text.lower()) \
        and ("saksikan" not in content.text.lower())
    ]
    return " ".join(content_clr)

###### Main ######
def scraper(category, url, delay, dt, excluded_url, producer):
    log = Logger("okezone", category, delay=delay, url=url)

    # Go to initial point
    log.log_start()
    [current_url, page_html] = navigate_page(url, delay, log, query={"date": dt})

    while(1):
        cnt = extract_all_news(producer, log, page_html, excluded_url, delay)
        log.add_news_count(cnt)

        next_url = get_next_index_page_url(page_html)
        if (next_url):
            [current_url, page_html] = navigate_page(next_url, delay, log)
        else:
            break

    log.log_finish()
    return log.export_report()
