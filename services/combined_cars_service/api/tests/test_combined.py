import pytest
from httpx import AsyncClient
from .. import main


@pytest.mark.anyio
async def test_get_all(test_db, headers):
    """
        Tests: 'get-all' endpoint
        Expected response code: 200
        Expected json: {'detail': 'Success storing cars and averages.'}
    """
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/combined/store-all',
                                headers=headers)
    assert response.status_code == 200
    assert response.json() == {'detail': 'Success storing cars and averages.'}
