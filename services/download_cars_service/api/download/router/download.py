from fastapi import HTTPException, Depends
from fastapi.security.api_key import APIKey
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
import requests

from ..auth.auth import get_api_key
from ..models import schemas

"""Download cars service implements the following endpoints :

1. '/' - check if Download car service is available,
2. '/cars/' - download information about cars from Mockachino API,
3. '/audi/' - download information about audi usage from Mockachino API,
4. '/porsche/' - download information about porsche usage from Mockachino API,
5. '/tesla/' - download information about tesla usage from Mockachino API.

"""


# Create router
download = InferringRouter()

# Header of every request sent to Mockachino API
headers = {'Content-type': 'application/json; charset=utf-8'}
# URL to Mockachino API
url = "https://www.mockachino.com/63df88f9-7c68-4e/"


@cbv(download)
class Download:
    # Injecting APIKey dependency
    api_key: APIKey = Depends(get_api_key)

    @download.get('/', status_code=200, include_in_schema=False)
    def download_check(self):
        """Check if"""
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
