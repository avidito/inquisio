from fastapi import APIRouter

from datetime import datetime

from application import database, settings

##### Router #####
router = APIRouter()

##### Endpoint #####
@router.get("/news", summary="Get news content")
def get_news(
    start_date: str = datetime.now().strftime("%Y-%m-%d"),
    end_date: str = datetime.now().strftime("%Y-%m-%d"),
    category: str = "all",
    src_category: str = "all",
    website: str = "all"
):
    return {
        "query": {
            "start_date": start_date,
            "end_date": end_date,
            "category": category,
            "src_category": src_category,
            "website": website
        },
        "headers": ["title", "author", "source", "url", "tags", "category", "src_category", "post_dt", "length", "content"],
        "rowcount": 1,
        "data": [
            ("test", "test", "test", "test", ["test", "test"], "test", "test", "2021-07-29", 2300, "testtesttesttesttest")
        ]
    }
