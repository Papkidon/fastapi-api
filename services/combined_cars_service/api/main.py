from fastapi import FastAPI

from .combined.models import models
from .combined.db.db import engine
from .combined.router.combined import combined

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url="/api/v1/combined/openapi.json", docs_url="/api/v1/combined/docs")

app.include_router(combined, prefix='/api/v1/combined', tags=['combined'])
