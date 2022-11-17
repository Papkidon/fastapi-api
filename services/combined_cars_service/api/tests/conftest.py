import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ...api import main
from ..combined.db.db import Base
from ..combined.router.combined import get_db

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
            "Authorization": str(os.getenv("API_KEY"))}


@pytest.fixture
def anyio_backend():
    """Asynchronous manner of testing"""
    return 'asyncio'
