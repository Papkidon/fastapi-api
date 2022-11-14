import pytest
from httpx import AsyncClient

from .. import main


@pytest.mark.anyio
async def test_query_porsche_usage(test_db, create_dummy_porsche_usage, headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/usage-data/porsche',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_query_audi_usage(test_db, create_dummy_audi_usage, headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/usage-data/audi',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_query_tesla_usage(test_db, create_dummy_tesla_usage, headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/usage-data/tesla',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_query_correct_cars_porsche_info(test_db, create_dummy_porsche_info, headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/car-info/porsche',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_query_correct_cars_audi_info(test_db, create_dummy_audi_info, headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/car-info/audi',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_query_correct_cars_tesla_info(test_db, create_dummy_tesla_info, headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/car-info/tesla',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_query_correct_cars_all_info(test_db,
                                           create_dummy_tesla_info,
                                           create_dummy_porsche_info,
                                           create_dummy_audi_info,
                                           headers):
    async with AsyncClient(app=main.app,base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/car-info/all',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_query_incorrect_cars_info(headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/car-info/maluch',
                                headers=headers)
    assert response.status_code == 422


# -------------------------- AVERAGE --------------------------

@pytest.mark.anyio
async def test_query_correct_cars_porsche_average(test_db, create_dummy_porsche_average, headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/average/porsche',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_query_correct_cars_tesla_average(test_db, create_dummy_tesla_average, headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/average/tesla',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_query_correct_cars_audi_average(test_db, create_dummy_audi_average, headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/average/audi',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_query_correct_cars_all_average(test_db,
                                              create_dummy_audi_average,
                                              create_dummy_tesla_average,
                                              create_dummy_porsche_average,
                                              headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/average/all',
                                headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_query_incorrect_average_info(headers):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/api/v1/query/average/maluch',
                                headers=headers)
    assert response.status_code == 404
