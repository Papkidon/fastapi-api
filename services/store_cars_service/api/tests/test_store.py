import pytest
from httpx import AsyncClient
from .. import main


@pytest.mark.anyio
async def test_store_correct_porsche(data_usage_correct,
                                     data_response_usage_correct,
                                     headers,
                                     test_db):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.post('/api/v1/store/usage/porsche',
                                 headers=headers,
                                 json=data_usage_correct)
    assert response.status_code == 201
    assert response.json() == data_response_usage_correct


@pytest.mark.anyio
async def test_store_incorrect_porsche(data_incorrect,
                                       headers,
                                       test_db):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.post('/api/v1/store/usage/porsche',
                                 headers=headers,
                                 json=data_incorrect)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_store_correct_audi(data_usage_correct,
                                  data_response_usage_correct,
                                  headers,
                                  test_db):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.post('/api/v1/store/usage/audi',
                                 headers=headers,
                                 json=data_usage_correct)
    assert response.status_code == 201
    assert response.json() == data_response_usage_correct


@pytest.mark.anyio
async def test_store_incorrect_audi(data_incorrect,
                                    headers,
                                    test_db):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.post('/api/v1/store/usage/audi',
                                 headers=headers,
                                 json=data_incorrect)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_store_correct_tesla(data_usage_correct,
                                   data_response_usage_correct,
                                   headers,
                                   test_db):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.post('/api/v1/store/usage/tesla',
                                 headers=headers,
                                 json=data_usage_correct)
    assert response.status_code == 201
    assert response.json() == data_response_usage_correct


@pytest.mark.anyio
async def test_store_incorrect_tesla(data_incorrect,
                                     headers,
                                     test_db):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.post('/api/v1/store/usage/tesla',
                                 headers=headers,
                                 json=data_incorrect)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_store_correct_cars(data_correct_cars,
                                  data_correct_response_cars,
                                  headers,
                                  test_db):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.post('/api/v1/store/cars/',
                                 headers=headers,
                                 json=data_correct_cars)
    assert response.status_code == 201
    assert response.json() == data_correct_response_cars


@pytest.mark.anyio
async def test_store_incorrect_cars(data_incorrect,
                                    headers,
                                    test_db):
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.post('/api/v1/store/cars/',
                                 headers=headers,
                                 json=data_incorrect)
    assert response.status_code == 422
