from fastapi import FastAPI

from .combined.models import models
from .combined.db.db import engine
from .combined.router.combined import combined

# Create tables if they don't exist already
models.Base.metadata.create_all(bind=engine)

# Create main app
app = FastAPI(openapi_url="/api/v1/combined/openapi.json", docs_url="/api/v1/combined/docs")

# Include combined router to the main app
app.include_router(combined, prefix='/api/v1/combined', tags=['combined'])
