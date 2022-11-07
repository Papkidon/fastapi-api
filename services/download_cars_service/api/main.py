from fastapi import FastAPI

from .download.router.download import download

app = FastAPI(openapi_url="/api/v1/download/openapi.json", docs_url="/api/v1/download/docs")

app.include_router(download, prefix='/api/v1/download', tags=['download'])
