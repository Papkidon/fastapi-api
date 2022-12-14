import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from ..query.db.connect.db import Base
from ..query.models.models import Porsche, Audi, Tesla, Cars, Average

from .. import main
from ..query.router.query import get_db

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
def headers():
    """Fixture for testing with request headers"""
    return {"Content-Type": "application/json",
            "Authorization": os.getenv("API_KEY")}


@pytest.fixture()
def create_dummy_porsche_usage():
    """Fixture for creating porsche usage dummy record and adds it to the database"""
    database = next(override_get_db())
    porsche = Porsche(id=1,
                      vin='DUMMY',
                      datetime=datetime.datetime.strptime('2020-01-10T11:00:00', '%Y-%m-%dT%H:%M:%S'),
                      soc=1,
                      chargingPower=5,
                      status='active')
    database.add(porsche)
    database.commit()

    yield


@pytest.fixture()
def create_dummy_audi_usage():
    """Fixture for creating audi usage dummy record and adds it to the database"""
    database = next(override_get_db())
    new = Audi(id=1,
               vin='DUMMY',
               datetime=datetime.datetime.strptime('2020-01-10T11:00:00', '%Y-%m-%dT%H:%M:%S'),
               soc=1,
               chargingPower=5,
               status='active')
    database.add(new)
    database.commit()

    yield


@pytest.fixture()
def create_dummy_tesla_usage():
    """Fixture for creating tesla usage dummy record and adds it to the database"""
    database = next(override_get_db())
    new = Tesla(id=1,
                vin='DUMMY',
                datetime=datetime.datetime.strptime('2020-01-10T11:00:00', '%Y-%m-%dT%H:%M:%S'),
                soc=1,
                chargingPower=5,
                status='active')
    database.add(new)
    database.commit()

    yield


@pytest.fixture()
def create_dummy_porsche_info():
    """Fixture for creating porsche info/usage dummy record and adds it to the database"""
    database = next(override_get_db())
    # Create new porsche usage data
    new = Porsche(id=1,
                  vin='PL110212',
                  datetime=datetime.datetime.strptime('2020-01-10T11:00:00', '%Y-%m-%dT%H:%M:%S'),
                  soc=1,
                  chargingPower=5,
                  status='active')
    database.add(new)
    database.commit()
    # Create new porsche information
    info = Cars(id=1,
                made="DummyCar",
                model="Dummy",
                year=datetime.datetime.now().date(),
                vin="PL110212")
    database.add(info)
    database.commit()

    yield


@pytest.fixture()
def create_dummy_audi_info():
    """Fixture for creating audi info/usage dummy record and adds it to the database"""
    database = next(override_get_db())
    # Create new porsche usage data
    new = Audi(id=2,
               vin='PL990011',
               datetime=datetime.datetime.strptime('2020-01-10T11:00:00', '%Y-%m-%dT%H:%M:%S'),
               soc=1,
               chargingPower=5,
               status='active')
    database.add(new)
    database.commit()
    # Create new porsche information
    info = Cars(id=2,
                made="DummyCar",
                model="Dummy",
                year=datetime.datetime.now().date(),
                vin="PL990011")
    database.add(info)
    database.commit()

    yield


@pytest.fixture()
def create_dummy_tesla_info():
    """Fixture for creating tesla info/usage dummy record and adds it to the database"""
    database = next(override_get_db())
    # Create new porsche usage data
    new = Tesla(id=3,
                vin='PL090201',
                datetime=datetime.datetime.strptime('2020-01-10T11:00:00', '%Y-%m-%dT%H:%M:%S'),
                soc=1,
                chargingPower=5,
                status='active')
    database.add(new)
    database.commit()
    # Create new porsche information
    info = Cars(id=3,
                made="DummyCar",
                model="Dummy",
                year=datetime.datetime.now().date(),
                vin="PL090201")
    database.add(info)
    database.commit()

    yield


@pytest.fixture()
def create_dummy_porsche_average():
    """Fixture for creating porsche average dummy record and adds it to the database"""
    database = next(override_get_db())
    # Create new porsche usage data
    new = Average(id=1,
                  vin="PL110212",
                  average=5)
    database.add(new)
    database.commit()

    yield


@pytest.fixture()
def create_dummy_audi_average():
    """Fixture for creating audi average dummy record and adds it to the database"""
    database = next(override_get_db())
    # Create new porsche usage data
    new = Average(id=2,
                  vin="PL990011",
                  average=5)
    database.add(new)
    database.commit()

    yield


@pytest.fixture()
def create_dummy_tesla_average():
    """Fixture for creating tesla average dummy record and adds it to the database"""
    database = next(override_get_db())
    # Create new porsche usage data
    new = Average(id=3,
                  vin="PL090201",
                  average=5)
    database.add(new)
    database.commit()

    yield


@pytest.fixture
def anyio_backend():
    """Asynchronous manner of testing"""
    return 'asyncio'
