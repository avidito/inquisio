import re
from datetime import datetime

def cvt_lowercase(data):
    """Convert columns value to lowercase"""

    result = {
        "title": data["title"].lower(),
        "category": data["category"].lower(),
        "author": data["author"].lower(),
        "post_dt": data["post_dt"],
        "tags": [v.lower() for v in data["tags"]],
        "content": data["content"].lower(),
        "url": data["url"]
    }
    return result

def clr_exc_whitespace(data):
    """Remove execessive whitespace"""

    clr = lambda value: re.sub(r"([ ]{2,}|[\n\r])", " ", value.strip())
    result = {
        "title": clr(data["title"]),
        "category": clr(data["category"]),
        "author": clr(data["author"]),
        "post_dt": data["post_dt"],
        "tags": [clr(v) for v in data["tags"]],
        "content": clr(data["content"]),
        "url": data["url"]
    }
    return result

def cvt_ts_to_datetime(data):
    """Convert timestamps to datetime string format"""

    cvt = lambda value: datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")
    result = {
        "title": data["title"],
        "category": data["category"],
        "author": data["author"],
        "post_dt": cvt(data["post_dt"]),
        "tags": data["tags"],
        "content": data["content"],
        "url": data["url"]
    }
    return result
