import requests
import time
from bs4 import BeautifulSoup

from . import Logger, reformat_dt, cvt_ts, check_url
from . import export_news # For testing purpose

###### Navigation ######
def navigate_page(url, delay, log, query=None, path=None, data=None):
    """Navigate to new page"""

    # Get page html
    req = requests.get(url, params=query)
    log.log_navigation(req.url, req.status_code, delay)
    time.sleep(delay)
    return req.url, BeautifulSoup(req.content, "lxml")

###### Extraction ######
def extract_all_news(producer, log, page, excluded_url, delay, mode):
    """Extract all news provided in current page"""

    news_list = page.find("div", attrs={"class": "indeks-news"}).find_all("div", attrs={"class": "indeks-rows"})
    cnt = 0
    for news in news_list:
        news_data = extract_news(news, delay, excluded_url, log)
        if (news_data):
            producer.publish_data(news_data)
            if (mode == "debug"):
                export_news(news_data)
            cnt += 1
    return cnt

def extract_news(news, delay, excluded_url, log):
    """Extract information from single news"""

    # Begin Extraction
    title = news.find("div", attrs={"class": "indeks-title"}).text
    category = news.find("div", attrs={"class": "mini-info"}).find("li").text
    url = news.find("div", attrs={"class": "indeks-title"}).a["href"]
    post_dt = cvt_ts(news.find("div", attrs={"class": "mini-info"}).find("p").text)

    # If URL is included in excluded_url
    info = extract_news_content(url, excluded_url, delay, log)
    if (info is None):
        return None

    news_data = {"title": title, "category": category, "author": info["author"], "post_dt": post_dt, "tags": info["tags"], "content": info["content"], "url": url}
    return news_data

def extract_news_content(url, excluded_url, delay, log):
    """Extracting more detail information from news article page"""

    [current_url, news_html] = navigate_page(url, delay, log, query={"showpage": "all"})
    if (not check_url(current_url, excluded_url)):
        return None

    # Author
    author_block = news_html.find("a", attrs={"rel": "author"})
    author = author_block.text if (author_block) else news_html.find("div", attrs={"class": "author"}).text

    # Tags
    tags_list_block = news_html.find("div", attrs={"class": "tag-list"})
    if (tags_list_block):
        tags_list = tags_list_block
    else:
        tags_list = news_html.find("div", attrs={"class": "category-relative"})
    tags = [tag.text for tag in tags_list.find_all("li")]

    content = extract_paginate_content(news_html, delay, log)

    return {"author": author, "tags": tags, "content": content}

def extract_paginate_content(page, delay, log):
    """Extract news content"""

    page_article = page.find("div", {"id": "content"})
    if (page_article is None):
        page_article = page.find("div", {"class": "article"})
    content = ops_clear_nonnews(page_article)

    return content

###### Get Element ######
def get_next_index_page_url(page):
    """Get next page url from next button"""

    next_button = page.find("a", attrs={"rel": "next"})
    next_url = next_button["href"] if (next_button) else None
    return next_url

###### Operations ######
def ops_clear_nonnews(content_blocks):
    """Clear non-news (e.g., ads, another news link) from content"""

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
def scraper(category, url, delay, dt, excluded_url, producer, mode):
    log = Logger("sindonews", category, delay=delay, url=url)

    # Go to initial point
    log.log_start()
    [current_url, page_html] = navigate_page(url, delay, log, query={"t": dt})

    while(1):
        cnt = extract_all_news(producer, log, page_html, excluded_url, delay, mode)
        log.add_news_count(cnt)

        next_url = get_next_index_page_url(page_html)
        if (next_url):
            [current_url, page_html] = navigate_page(next_url, delay, log, mode)
        else:
            break

    log.log_finish()
    return log.export_report()
