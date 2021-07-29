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

    news_list = page.find_all("div", attrs={"class": "article__list"})
    cnt = 0
    for news in news_list:
        try:
            news_data = extract_news(news, delay, excluded_url, log)
            if (news_data):
                producer.publish_data(news_data)
                if (mode == "debug"):
                    export_news(news_data) # For testing purpose
                cnt += 1
        except Exception as e:
            log.log_error(f"Failed to extract news >> {str(e)}")
    return cnt

def extract_news(news, delay, excluded_url, log):
    """Extract information from single news"""

    # Begin Extraction
    title = news.find("h3", attrs={"class": "article__title"}).text
    website = log.website
    channel = log.category
    category = news.find("div", attrs={"class": "article__subtitle"}).text
    url = news.find("a", attrs={"class": "article__link"}).get("href")
    post_dt = cvt_ts(news.find("div", attrs={"class": "article__date"}).text)

    # If URL is included in excluded_url
    info = extract_news_content(url, excluded_url, delay, log)
    if (info is None):
        return None

    news_data = {"title": title, "website": website, "channel": channel, "category": category, "author": info["author"], "post_dt": post_dt, "tags": info["tags"], "content": info["content"], "url": url}
    return news_data

def extract_news_content(url, excluded_url, delay, log):
    """Extracting more detail information from news article page"""

    [current_url, news_html] = navigate_page(url, delay, log, query={"page": "all"})
    if (not check_url(current_url, excluded_url)):
        return None

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
    content = extract_paginate_content(news_html, delay, log)

    return {"author": author_clr, "tags": tags, "content": content}

def extract_paginate_content(page, delay, log):
    """Extract news content"""

    page_article = [p.text for p in page.find("div", attrs={"class": "read__content"}).find_all(["p", "ul", "ol"], recursive=False)]
    content = ops_clear_nonnews(page_article)

    return content

###### Get Element ######
def get_next_index_page_url(page):
    """Get next page url from next button"""

    next_button = page.find("a", attrs={"class": "paging__link"}, string="Next")
    next_url = next_button.get("href") if (next_button) else None
    return next_url

###### Operations ######
def ops_clear_nonnews(content_blocks):
    """Clear non-news (e.g., ads, another news link) from content"""

    content_clr = [
        content for content in content_blocks
        if (not content.lower().startswith("baca juga"))
    ]
    return " ".join(content_clr)

###### Main ######
def scraper(category, url, delay, dt, excluded_url, producer, mode):
    log = Logger("kompas", category, delay=delay, url=url)

    # Go to initial point
    log.log_start()
    [current_url, page_html] = navigate_page(url, delay, log, query={"date": dt})

    while(1):
        cnt = extract_all_news(producer, log, page_html, excluded_url, delay, mode)
        log.add_news_count(cnt)

        next_url = get_next_index_page_url(page_html)
        if (next_url):
            [current_url, page_html] = navigate_page(next_url, delay, log)
        else:
            break

    log.log_finish()
    return log.export_report()
