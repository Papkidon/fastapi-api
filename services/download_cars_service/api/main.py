from fastapi import FastAPI

from .download.router.download import download

# Create main FastAPI app
app = FastAPI(openapi_url="/api/v1/download/openapi.json", docs_url="/api/v1/download/docs")

# Include download router to the main FastAPI app
app.include_router(download, prefix='/api/v1/download', tags=['download'])
