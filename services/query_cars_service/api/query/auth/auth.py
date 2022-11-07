from fastapi.security.api_key import APIKeyHeader
from fastapi import HTTPException, Security
import os

API_KEY = os.getenv('API_KEY')
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(
        api_key_header: str = Security(api_key_header),
):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403)
