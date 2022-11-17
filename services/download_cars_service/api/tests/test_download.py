import pytest
from httpx import AsyncClient

from ...api import main


@pytest.mark.anyio
async def test_download_porsche(headers):
    """
    Tests endpoint: '/porsche/',
    Expected response code: 200
    """
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/download/porsche/',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_download_audi(headers):
    """
    Tests endpoint: '/audi/',
    Expected response code: 200
    """
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/download/audi/',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_download_tesla(headers):
    """
    Tests endpoint: '/tesla/',
    Expected response code: 200
    """
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/download/tesla/',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_download_incorrect_car(headers):
    """
    Tests incorrect endpoint: '/maluch/',
    Expected response code: 404
    """
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/download/maluch/',
                                headers=headers)
    assert response.status_code == 404
