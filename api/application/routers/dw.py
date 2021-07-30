from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from datetime import datetime

from application.database import engine, query

##### Router #####
router = APIRouter(
    prefix = "/summary"
)
get_db = engine.session_factory()

##### Endpoint #####
@router.get("/news", summary="Get news count per website and category")
def get_news_cnt(
    day: str = datetime.now().strftime("%Y-%m-%d"),
    category: str = "all",
    src_category: str = "all",
    website: str = "all",
    db: Session = Depends(get_db)
):
    query_params = {
        "day": day,
        "category": category,
        "src_category": src_category,
        "website": website
    }
    rowcount, data = query.get_news_cnt(db, query_params)
    return {
        "query_params": query_params,
        "rowcount": rowcount,
        "data": data
    }

@router.get("/tags", summary="Get tags count from each website")
def get_tags_cnt(
    day: str = datetime.now().strftime("%Y-%m-%d"),
    website: str = "all",
    db: Session = Depends(get_db)
):
    query = {
        "day": day,
        "website": website
    }
    header = ["website", "tags", "day", "cnt"]
    rowcount = 1
    data = [
        ("test", "test", "test", 100)
    ]
    return {
        "query": query,
        "header": header,
        "rowcount": rowcount,
        "data": data
    }
