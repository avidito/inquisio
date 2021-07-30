from sqlalchemy import text, inspect, and_
from datetime import datetime
from .models import News, Categories

def row_as_dict(row):
    row_dict = {
        col.key : getattr(row, col.key) \
        for col in inspect(row).mapper.column_attrs
    }
    return row_dict

##### SRC #####
def get_news(db, params):
    """Get news information along with its category and contents"""

    # Embed regex pattern columns with start and end tag
    regex_pattern_columns = ["category", "src_category", "website", "channel"]
    fmt_params = {}
    for col in params.keys():
        if (col in regex_pattern_columns):
            fmt_params[col] = params[col] if (params[col] != "all") else "%"
        else:
            fmt_params[col] = params[col]
    start_date = fmt_params["start_date"]
    end_date = fmt_params["end_date"]
    category = fmt_params["category"]
    src_category = fmt_params["src_category"]
    website = fmt_params["website"]
    channel = fmt_params["channel"]

    # Execute query
    results = db.query(
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
    ).all()
    return results
