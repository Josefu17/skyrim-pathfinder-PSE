"""contains common fixtures that are detected by other test files automatically"""

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.database.schema.base import Base

# Create a new engine for the in-memory SQLite database with foreign keys enabled
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function", name="db")
def test_db():
    """Create a RAM-Database with foreign keys enforced and scoped to each individual test"""
    # Set up the test database (create all tables)
    with engine.connect() as connection:
        # Enable foreign key support for SQLite
        connection.execute(text("PRAGMA foreign_keys=ON"))

    # Create tables after enabling foreign keys
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    session.close()
    # Tear down the database (drop all tables)
    Base.metadata.drop_all(engine)
