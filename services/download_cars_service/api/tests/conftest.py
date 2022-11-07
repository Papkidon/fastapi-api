import pytest
import os
from fastapi.testclient import TestClient

from ...api import main

client = TestClient(main.app)


@pytest.fixture
def headers():
    return {'Content-Type': 'application/json',
            'Authorization': str(os.getenv('API_KEY'))}


@pytest.fixture
def anyio_backend():
    return 'asyncio'
