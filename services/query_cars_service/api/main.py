from fastapi import FastAPI

from .query.router.query import query

# Create main FastAPI app
app = FastAPI(openapi_url="/api/v1/query/openapi.json", docs_url="/api/v1/query/docs")

# Include download router to the main FastAPI app
app.include_router(query, prefix='/api/v1/query', tags=['query'])
