from sqlalchemy import text, inspect
from .models import News

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

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
    website = fmt_params["website"]

    # Execute query
    query_result = db.query(News).filter(News.website.like(website))
    header = list(object_as_dict(query_result.first()).keys())
    data = [[value for col, value in object_as_dict(result).items()] for result in query_result.all()] if (query_result) else []
    return header, data
