from fastapi import HTTPException, Depends
from fastapi.security.api_key import APIKey
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
import requests

from ..auth.auth import get_api_key
from ..models import schemas

download = InferringRouter()

headers = {'Content-type': 'application/json; charset=utf-8'}
url = "https://www.mockachino.com/63df88f9-7c68-4e/"


@cbv(download)
class Download:
    api_key: APIKey = Depends(get_api_key)

    @download.get('/', status_code=200, include_in_schema=False)
    def download_check(self):
        return {'detail': 'Download service is up.'}

    @download.get("/cars/", status_code=200, response_model=schemas.CarInfo)
    async def download_cars(self):
        """
        Download information about cars from Mockachino API.
        """
        response = requests.get(f"{url}/evs", headers=headers)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=404, detail="Resource not found.")

    @download.get("/audi/", status_code=200, response_model=schemas.UsageData)
    async def download_audi(self):
        """
        Download information about audi car usage from Mockachino API.
        """
        response = requests.get(f"{url}/evs/PL990011", headers=headers)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=404, detail="Resource not found.")

    @download.get("/porsche/", status_code=200, response_model=schemas.UsageData)
    async def download_porsche(self):
        """
        Download information about porsche car usage from Mockachino API.
        """
        response = requests.get(f"{url}/evs/PL110212", headers=headers)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=404, detail="Resource not found.")

    @download.get("/tesla/", status_code=200, response_model=schemas.UsageData)
    async def download_tesla(self):
        """
        Download information about tesla car usage from Mockachino API.
        """
        response = requests.get(f"{url}/evs/PL090201", headers=headers)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=404, detail="Resource not found.")
