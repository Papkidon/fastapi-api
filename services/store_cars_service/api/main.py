from fastapi import FastAPI

from .store.models import models
from .store.db.db import engine
from .store.router.store import store

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url="/api/v1/store/openapi.json", docs_url="/api/v1/store/docs")

app.include_router(store, prefix='/api/v1/store', tags=['store'])
