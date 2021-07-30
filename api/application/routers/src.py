from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from datetime import datetime

from application.database import engine, query

router = APIRouter()
get_db = engine.session_factory()

##### Endpoint #####
@router.get("/news", summary="Get news content")
def get_news(
    start_date: str = datetime.now().strftime("%Y-%m-%d"),
    end_date: str = datetime.now().strftime("%Y-%m-%d"),
    category: str = "all",
    src_category: str = "all",
    website: str = "all",
    channel: str = "all",
    db: Session = Depends(get_db)
):
    query_params = {
        "start_date": start_date,
        "end_date": end_date,
        "category": category,
        "src_category": src_category,
        "website": website,
        "channel": channel
    }
    header, data = query.get_news(db, query_params)

    rowcount = 1
    return {
        "query_params": query_params,
        "headers": header,
        "rowcount": rowcount,
        "data": data
    }
