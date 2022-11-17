import pytest
import os
from fastapi.testclient import TestClient

from ...api import main

# New test client for main app
client = TestClient(main.app)


@pytest.fixture
def headers():
    """Fixture for testing client containing headers for every request"""
    return {'Content-Type': 'application/json',
            'Authorization': str(os.getenv('API_KEY'))}


@pytest.fixture
def anyio_backend():
    """Asynchronous manner of testing"""
    return 'asyncio'
