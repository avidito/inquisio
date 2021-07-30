from sqlalchemy import text, inspect, and_
from datetime import datetime
from sqlalchemy.dialects import postgresql

from .models import News, Categories, NewsCnt

##### SQL #####
## SRC SQL ##
def execute_get_news(db, start_date, end_date, category, src_category, website, channel):
    """Executing get_news query logic"""

    query = db.query(
        News.title,
        News.website,
        Categories.channel,
        Categories.category,
        Categories.src_category,
        News.author,
        News.url,
        News.post_dt
    ).select_from(
        News
    ).join(
        Categories,
        News.category_id == Categories.category_id,
        isouter = True
    ).filter(
        and_(
            News.post_dt >= start_date,
            News.post_dt <= end_date,
            Categories.category.like(category),
            Categories.src_category.like(src_category),
            News.website.like(website),
            Categories.channel.like(channel)
        )
    )
    return query.all()

## DW SQL ##
def execute_get_news_cnt(db, day, category, src_category, website):
    """Execute get_news_cnt query logic"""

    query = db.query(
        NewsCnt.website,
        NewsCnt.category,
        NewsCnt.src_category,
        NewsCnt.day,
        NewsCnt.cnt
    ).select_from(
        NewsCnt
    ).filter(
        and_(
            NewsCnt.day == day,
            NewsCnt.category.like(category),
            NewsCnt.src_category.like(src_category),
            NewsCnt.website.like(website)
        )
    )
    return query.all()

##### Utils #####
def convert_regex_pattern_columns(params, convert_list):
    """Convert string query params to support LIKE filter"""

    fmt_params = {}
    for col in params.keys():
        if (col in convert_list):
            fmt_params[col] = params[col] if (params[col] != "all") else "%"
        else:
            fmt_params[col] = params[col]
    return fmt_params
