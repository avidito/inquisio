from fastapi import APIRouter

from datetime import datetime

from application import database, settings

##### Router #####
router = APIRouter(
    prefix = "/summary"
)

##### Endpoint #####
@router.get("/news", summary="Get news count per website and category")
def get_news_cnt(
    day: str = datetime.now().strftime("%Y-%m-%d"),
    category: str = "all",
    src_category: str = "all",
    website: str = "all"
):
    return {
        "query": {
            "day": day,
            "category": category,
            "src_category": src_category,
            "website": website
        },
        "headers": ["website", "category", "src_category", "day", "cnt"],
        "rowcount": 1,
        "data": [
            ("test", "test", "test", "test", 100)
        ]
    }

@router.get("/tags", summary="Get tags count from each website")
def get_news(
    day: str = datetime.now().strftime("%Y-%m-%d"),
    website: str = "all"
):
    return {
        "query": {
            "day": day,
            "website": website
        },
        "headers": ["website", "tags", "day", "cnt"],
        "rowcount": 1,
        "data": [
            ("test", "test", "test", 100)
        ]
    }
