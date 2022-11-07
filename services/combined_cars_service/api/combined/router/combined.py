import os

from fastapi import APIRouter, HTTPException, Depends
import requests
from fastapi.openapi.models import APIKey

from ..db.db import SessionLocal
# This will only work if all API keys are the same
from ..auth.auth import get_api_key

combined = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@combined.get('/', status_code=200, include_in_schema=False)
def combined_check():
    return {'detail': 'Combined service is up.'}


@combined.get('/store-all', status_code=200)
async def get_and_store_all(api_key: APIKey = Depends(get_api_key)):
    """Download from /download endpoint and store via /store endpoint all cars
    plus calculate the mean and store it too."""
    # Store all cars
    cars_list = [
        'porsche',
        'audi',
        'tesla',
        'cars'
    ]

    for car in cars_list:
        data = requests.get(f'http://download_cars_service:8000/api/v1/download/{car}/',
                            headers={'Content-Type': 'application/json',
                                     'Authorization': os.getenv('DOWNLOAD_API_KEY')}).json()
        if not data:
            raise HTTPException(status_code=404, detail='Error downloading cars.')
        store = requests.post(f'http://store_cars_service:8000/api/v1/store/{car}/',
                              headers={'Content-Type': 'application/json',
                                       'Authorization': os.getenv('STORE_API_KEY')},
                              json=data)
        if store.status_code == 201 or store.status_code == 409:
            continue
        else:
            raise HTTPException(status_code=404, detail='Error storing cars.')
    # Store averages
    data = requests.get(f'http://store_cars_service:8000/api/v1/store/average/',
                        headers={'Content-Type': 'application/json',
                                 'Authorization': os.getenv('STORE_API_KEY')})
    if data.status_code == 200 or data.status_code == 409:
        return {'detail': 'Success storing cars and averages.'}
    raise HTTPException(status_code=404, detail='Error storing cars and averages.')

