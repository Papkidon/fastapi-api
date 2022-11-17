import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import main
from ..store.db.connection.db import Base
from ..store.router.store import get_db

# New testing SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create new testing engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Create new testing session maker
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Yield testing db connection"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override main app dependencies with testing database connection
main.app.dependency_overrides[get_db] = override_get_db

# Create FastAPI TestClient instance
client = TestClient(main.app)


@pytest.fixture()
def test_db():
    """Fixture for creating tables,
    executing some code, and finally dropping all tables"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def anyio_backend():
    """Asynchronous manner of testing"""
    return 'asyncio'


@pytest.fixture()
def headers():
    """Fixture for testing with request headers"""
    return {'Content-Type': 'application/json',
            'Authorization': os.getenv('API_KEY')}


@pytest.fixture(scope='session')
def data_usage_correct():
    """Fixture for including usage data in test"""
    return \
        {
            "vin": "PL990011",
            "carStatistics": [
                {
                    "datetime": "2020-03-10T11:00:00",
                    "soc": "0",
                    "chargingPower": 0,
                    "status": "waiting"
                }
            ]
        }


@pytest.fixture(scope='session')
def data_response_usage_correct():
    """Fixture for including correct response of storing usage data in test"""
    return \
        [
            {'datetime': '2020-03-10T11:00:00',
             'soc': 0,
             'chargingPower': 0.0,
             'status': 'waiting',
             'vin': 'PL990011'
             }
        ]


@pytest.fixture(scope='session')
def data_response_correct():
    """Fixture for including correct response of usage data in test"""
    return \
        [
            {'chargingPower': 0.0,
             'datetime': '2022-10-30T09:58:51.587000',
             'soc': 0,
             'status': 'string',
             'vin': 'porsche'
             }
        ]


@pytest.fixture(scope='session')
def data_correct_cars():
    """Fixture for including correct car information in test"""
    return \
        {
            "cars": [
                {
                    "made": "Tesla",
                    "model": "Model S",
                    "year": "2020-08-10",
                    "vin": "PL090201"
                }
            ]
        }


@pytest.fixture(scope='session')
def data_correct_response_cars():
    """Fixture for including correct response of storing cars info in test"""
    return \
        [
            {
                'made': 'Tesla',
                'model': 'Model S',
                'year': '2020-08-10',
                'vin': 'PL090201'
            }
        ]


@pytest.fixture(scope='session')
def data_incorrect():
    """Fixture for including incorrect data to be stored in test"""
    return {"im": "bad"}
