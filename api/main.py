from fastapi import FastAPI

from application.routers import src, dw
from application.tags import tags_metadata


app = FastAPI(
    title = "Inquisio-API",
    description = "Inquisio data API",
    version = "0.1",
    openapi_tags = tags_metadata
)
app.include_router(src.router, tags=["SRC"])
app.include_router(dw.router, tags=["DW"])
