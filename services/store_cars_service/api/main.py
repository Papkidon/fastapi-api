from fastapi import FastAPI

from .store.models import models
from .store.db.connection.db import engine
from .store.router.store import store

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Create main FastAPI app
app = FastAPI(openapi_url="/api/v1/store/openapi.json", docs_url="/api/v1/store/docs")

# Include router in the main FastAPI app
app.include_router(store, prefix='/api/v1/store', tags=['store'])
