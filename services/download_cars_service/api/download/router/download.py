from fastapi import APIRouter, HTTPException, Depends
from ..models import schemas
from fastapi.security.api_key import APIKey
from ..auth.auth import get_api_key
import requests


download = APIRouter()

headers = {'Content-type': 'application/json; charset=utf-8'}
url = "https://www.mockachino.com/63df88f9-7c68-4e/"


@download.get('/', status_code=200, include_in_schema=False)
def download_check():
    return {'detail': 'Download service is up.'}


@download.get("/cars/", status_code=200, response_model=schemas.Car)
async def download_cars(api_key: APIKey = Depends(get_api_key)):
    """
    Download information about cars from Mockachino API.
    """
    response = requests.get(f"{url}/evs", headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=404, detail="Resource not found.")


@download.get("/audi/", status_code=200, response_model=schemas.CarStats)
async def download_audi(api_key: APIKey = Depends(get_api_key)):
    """
    Download information about audi car usage from Mockachino API.
    """
    response = requests.get(f"{url}/evs/PL990011", headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=404, detail="Resource not found.")


@download.get("/porsche/", status_code=200, response_model=schemas.CarStats)
async def download_porsche(api_key: APIKey = Depends(get_api_key)):
    """
    Download information about porsche car usage from Mockachino API.
    """
    response = requests.get(f"{url}/evs/PL110212", headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=404, detail="Resource not found.")


@download.get("/tesla/", status_code=200, response_model=schemas.CarStats)
async def download_tesla(api_key: APIKey = Depends(get_api_key)):
    """
    Download information about tesla car usage from Mockachino API.
    """
    response = requests.get(f"{url}/evs/PL090201", headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=404, detail="Resource not found.")
