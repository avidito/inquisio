from datetime import datetime
import re
import itertools

from .utils import vectorize, log_process

def processor(data):
    """Processor main function"""

    news_0 = data.copy()
    news_1 = cvt_lowercase(news_0)
    news_2 = cvt_ts_to_datetime(news_1)
    news_3 = clr_exc_whitespace(news_2)
    news_4 = add_news_tmp_id(news_3)
    contents_0 = crt_contents_dataset(news_4)
    tags_0 = crt_tags_dataset(news_4)
    categories_0 = crt_categories_dataset(news_4)
    map_news_tags_0 = crt_map_news_tags(news_4, tags_0)
    news_5 = upt_news_cols_and_fk(news_4, categories_0)

    return {
        "news": news_5,
        "contents": contents_0,
        "tags": tags_0,
        "categories": categories_0,
        "map_news_tags": map_news_tags_0
    }

########## Processing Functions ##########
##### Add #####
@log_process
def add_news_tmp_id(data):
    """Add temporary id for news data"""

    cnt = len(data["title"])
    result = {
        "news_id": [i for i in range(cnt)],
        **data
    }
    return result

##### Convert #####
@log_process
def cvt_lowercase(data):
    """Convert columns value to lowercase"""

    cvt_lc = vectorize(str.lower)
    result = {
        "title": cvt_lc(data["title"]),
        "category": cvt_lc(data["category"]),
        "author": cvt_lc(data["author"]),
        "post_dt": data["post_dt"],
        "tags": cvt_lc(data["tags"]),
        "content": cvt_lc(data["content"]),
        "url": data["url"]
    }
    return result

@log_process
def cvt_ts_to_datetime(data):
    """Convert timestamps to datetime string format"""

    cvt_ttd = vectorize(lambda value: datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M:%S"))
    result = {
        "title": data["title"],
        "category": data["category"],
        "author": data["author"],
        "post_dt": cvt_ttd(data["post_dt"]),
        "tags": data["tags"],
        "content": data["content"],
        "url": data["url"]
    }
    return result

##### Clear #####
@log_process
def clr_exc_whitespace(data):
    """Remove execessive whitespace"""

    clr_ews = vectorize(lambda value: re.sub(r"([ ]{2,}|[\n\r])", " ", value.strip()))
    result = {
        "title": clr_ews(data["title"]),
        "category": clr_ews(data["category"]),
        "author": clr_ews(data["author"]),
        "post_dt": data["post_dt"],
        "tags": clr_ews(data["tags"]),
        "content": clr_ews(data["content"]),
        "url": data["url"]
    }
    return result

##### Create #####
@log_process
def crt_contents_dataset(data):
    """Create contents dataset from news data"""

    # Create partitioned contents
    block_size = 1000
    contents = []
    for news_id in data["news_id"]:
        raw_content = data["content"][news_id]
        length = len(raw_content)

        pivot = 0
        p_id = 1
        while(pivot < length):
            partition = raw_content[pivot : pivot + block_size]
            contents.append((p_id, news_id, len(partition), partition))

            pivot += block_size

    # Convert to column format
    [partition_id, news_id, length, partition] = list(zip(*contents))
    result = {
        "partition_id": partition_id,
        "news_id": news_id,
        "length": length,
        "partition": partition
    }
    return result

@log_process
def crt_tags_dataset(data):
    """Create tags dataset from news data"""

    tags = set(itertools.chain(*data["tags"]))
    cnt = len(tags)
    result = {
        "tag_id": list(range(cnt)),
        "tag": list(tags)
    }
    return result

@log_process
def crt_categories_dataset(data):
    """Create categories dataset from news data"""

    categories = set(itertools.chain(data["category"]))
    cnt = len(categories)
    result = {
        "category_id": list(range(cnt)),
        "src_category": list(categories),
        "gen_category": "",
        "source": ""
    }
    return result

@log_process
def crt_map_news_tags(data_news, data_tags):
    """Create map_news_tags dataset from news and tags data"""

    # Create news tag mapping
    mapper = {tag: tag_id for tag, tag_id in zip(data_tags["tag"], data_tags["tag_id"])}
    map_news_tags = [
        (news_id, mapper[tag]) \
        for news_id in data_news["news_id"] for tag in data_news["tags"][news_id]
    ]

    # Convert to column format
    [news_id, tag_id] = list(zip(*map_news_tags))
    result = {
        "news_id": news_id,
        "tag_id": tag_id
    }
    return result

##### Update #####
@log_process
def upt_news_cols_and_fk(data_news, data_categories):
    """Update columns and foreign key for news data"""

    mapper = {ctg: ctg_id for ctg_id, ctg in zip(data_categories["category_id"], data_categories["src_category"])}
    category_id = [mapper[ctg] for ctg in data_news["category"]]

    result = {
        "news_id": data_news["news_id"],
        "category_id": category_id,
        "content_id": data_news["news_id"],
        "title": data_news["title"],
        "author": data_news["author"],
        "post_dt": data_news["post_dt"],
        "website": ""
    }
    return result
