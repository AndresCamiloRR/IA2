import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Ensure the backend package is importable
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_PATH = os.path.join(REPO_ROOT, "quicktask_backend")
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)


# Now import the project modules
import database as database


# Create an in-memory SQLite engine for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Replace the engine and SessionLocal in the project's database module so
# FastAPI / SQLAlchemy objects use the in-memory DB during tests.
database.engine = engine
database.SessionLocal = TestingSessionLocal


# Import models (they rely on database.Base)
import models  # noqa: E402


# Create all tables in the in-memory DB
database.Base.metadata.create_all(bind=engine)


# Import the FastAPI app after the DB has been configured
import main as main  # noqa: E402


def override_get_db():
    """Yield a database session for FastAPI dependency override."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the dependency used by the app (main.get_db)
main.app.dependency_overrides[main.get_db] = override_get_db


from fastapi.testclient import TestClient
import pytest


@pytest.fixture(scope="session")
def client():
    """Provide a TestClient instance configured to use the in-memory DB."""
    with TestClient(main.app) as c:
        yield c


@pytest.fixture(scope="function")
def db_session():
    """Provide a clean DB session for tests that need direct DB access."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
