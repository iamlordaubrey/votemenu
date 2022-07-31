import pytest

from sqlalchemy.orm import Session
from sqlalchemy_utils.functions import database_exists, drop_database, create_database

from app.database import Base, testing_engine, override_get_db, TestingSessionLocal, get_db
from app.server import app
from app.settings import settings


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    Create a clean database on every test case.
    We use the `sqlalchemy_utils` package here for a few helpers in consistently
    creating and dropping the database.
    """
    if database_exists(settings.test_db_dsn):
        drop_database(settings.test_db_dsn)
    create_database(settings.test_db_dsn)  # Create the test database.
    Base.metadata.create_all(testing_engine)  # Create the tables.
    app.dependency_overrides[get_db] = override_get_db  # Mock the Database Dependency
    yield  # Run the tests.
    drop_database(settings.test_db_dsn)  # Drop the test database.


@pytest.yield_fixture(scope="session", autouse=True)
def test_db_session():
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    session: Session = TestingSessionLocal()
    yield session
    # Drop all data after each test
    for tbl in reversed(Base.metadata.sorted_tables):
        testing_engine.execute(tbl.delete())
    # put back the connection to the connection pool
    session.close()
