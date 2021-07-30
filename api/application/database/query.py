from .sql import convert_regex_pattern_columns
from .sql import (
    execute_get_news,
    execute_get_news_cnt,
    execute_get_tags_cnt
)

##### SRC #####
def get_news(db, params):
    """Get news information along with its category and contents"""

    fmt_params = convert_regex_pattern_columns(params, ["category", "src_category", "website", "channel"])
    results = execute_get_news(db, **fmt_params)
    rowcount = len(results) if (results) else 0
    return rowcount, results

##### DW #####
def get_news_cnt(db, params):
    """Get news count summary"""

    fmt_params = convert_regex_pattern_columns(params, ["category", "src_category", "website"])
    results = execute_get_news_cnt(db, **fmt_params)
    rowcount = len(results) if (results) else 0
    return rowcount, results

def get_tags_cnt(db, params):
    """Get tags count summary"""

    fmt_params = convert_regex_pattern_columns(params, ["website"])
    results = execute_get_tags_cnt(db, **fmt_params)
    rowcount = len(results) if (results) else 0
    return rowcount, results
