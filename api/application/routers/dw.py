from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from datetime import datetime

from application.database import engine, models

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
    query = {
        "day": day,
        "category": category,
        "src_category": src_category,
        "website": website
    }
    header = ["website", "category", "src_category", "day", "cnt"]
    rowcount = 1
    data = [
        ("test", "test", "test", "test", 100)
    ]
    return {
        "query": query,
        "header": header,
        "rowcount": rowcount,
        "data": data
    }

@router.get("/tags", summary="Get tags count from each website")
def get_news(
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
