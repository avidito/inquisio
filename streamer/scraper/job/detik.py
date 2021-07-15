import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

from . import Logger, reformat_dt, export_news

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
    post_dt = news.find("div", attrs={"class": "media__date"}).span.get("d-time")

    info = extract_news_content(url, delay, log)

    news_data = {"title": title, "category": info["category"], "author": info["author"], "post_dt": post_dt, "tags": info["tags"], "content": info["content"], "url": url}
    export_news(news_data)

def extract_news_content(url, delay, log):
    """Extracting more detail information from news article page"""

    params = {"single": "1"}

    [current_url, news_html] = navigate_page(url, delay, log, params)

    # Category
    category = news_html.find("div", attrs={"class": "page__breadcrumb"}).find_all("a")[-1].text

    # Author
    author_block = news_html.find("div", attrs={"class": "detail__author"}).text
    author = author_block.split(" - ")[0]

    # Tags
    tags = [tag.text for tag in news_html.find_all("a", attrs={"class": "nav__item"})]

    # Content
    content = extract_paginate_content(news_html, delay, log)

    return {"category": category, "author": author, "tags": tags, "content": content}

def extract_paginate_content(page, delay, log):
    """Extract news content"""

    content = []
    page_article = page.find("div", attrs={"class": "detail__body-text"})
    
    content.append(page_article.find("strong").text)
    content.append(page_article.find("strong").next_sibling.string)
    content.extend([p.text for p in page_article.find_all("p")])

    return " ".join(content)

###### Get Element ######
def get_next_index_page_url(page):
    """Get next page url from next button"""

    next_button = page.find("a", string="Next")
    next_url = next_button.get("href")
    return next_url

###### Main ######
def scraper(category, url, delay, dt, producer):
    log = Logger("detik", category, delay=delay, url=url)
    all_news_cnt = 0

    params = {"date": reformat_dt(dt, "%Y-%m-%d", "%m/%d/%Y")}

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
