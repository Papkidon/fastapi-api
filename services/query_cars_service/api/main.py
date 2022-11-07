from fastapi import FastAPI

from .query.router.query import query

app = FastAPI(openapi_url="/api/v1/query/openapi.json", docs_url="/api/v1/query/docs")

app.include_router(query, prefix='/api/v1/query', tags=['query'])
