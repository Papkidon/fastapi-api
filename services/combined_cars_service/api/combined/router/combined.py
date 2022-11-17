from fastapi import HTTPException, Depends
from fastapi.openapi.models import APIKey
from fastapi_utils.inferring_router import InferringRouter
from ..db.db import SessionLocal
from ..auth.auth import get_api_key
from fastapi_utils.cbv import cbv
import requests
import os

"""Combined cars service implements the following endpoints : 

1. '/' - returns 'Combined service is up' when service is reachable,
2. '/store-all' - download cars through Download cars service and store them via Store cars service.

"""

combined = InferringRouter()


def get_db():
    """Get new database connection from connection pool
    and close after code execution"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def download_and_store(download: str, store: str) -> None:
    """Download and store cars in the database
    :param: download: string with Download cars service endpoint
    :param: store: string with Store cars service endpoint
    :return: None: if successful, else throws some exception
    """
    headers_download = {'Content-Type': 'application/json',
                        'Authorization': os.getenv('DOWNLOAD_API_KEY')}
    headers_store = {'Content-Type': 'application/json',
                     'Authorization': os.getenv('STORE_API_KEY')}

    download_cars = requests.get(f'http://download_cars_service:8000/api/v1/download/{download}',
                                 headers=headers_download).json()
    if not download_cars:
        raise HTTPException(status_code=404, detail='Error downloading cars.')
    store_cars = requests.post(f'http://store_cars_service:8000/api/v1/store/{store}',
                               headers=headers_store,
                               json=download_cars)
    if store_cars.status_code not in (201, 409):
        raise HTTPException(status_code=404, detail='Error storing cars.')


@cbv(combined)
class Combined:
    api_key: APIKey = Depends(get_api_key)

    @combined.get('/', status_code=200, include_in_schema=False)
    def combined_check(self):
        return {'detail': 'Combined service is up.'}

    @combined.get('/store-all', status_code=200)
    async def get_and_store_all(self):
        """Download from /download endpoint and store via /store endpoint all cars
        plus calculate the mean and store it too."""

        # Store cars info
        download_and_store("cars/", "cars/")

        # Store porsche
        download_and_store("porsche/", "usage/porsche/")

        # Store audi
        download_and_store("audi/", "usage/audi/")

        # Store tesla
        download_and_store("tesla/", "usage/tesla/")

        # Store averages
        data = requests.get(f'http://store_cars_service:8000/api/v1/store/average/',
                            headers={'Content-Type': 'application/json',
                                     'Authorization': os.getenv('STORE_API_KEY')})
        if data.status_code == 200 or data.status_code == 409:
            return {'detail': 'Success storing cars and averages.'}
        raise HTTPException(status_code=404, detail='Error storing cars and averages.')
