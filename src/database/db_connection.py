"""handles connection sessions to the database"""

from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

USER = "pg-2"
PASSWORD = "pg-2"
HOST = "postgres"
PORT = "5432"
DB_NAME = "navigation"

engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
)

SessionLocal = sessionmaker(bind=engine)


@contextmanager
def get_db_session():
    """getter for db session with the configured parameters"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def with_db_session(func):
    """defines @with_db_session context manager decorator to auto-inject db session"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        with get_db_session() as session:
            kwargs["session"] = session
            return func(*args, **kwargs)

    return wrapper
