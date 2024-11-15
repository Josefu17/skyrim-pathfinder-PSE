"""
ORM Behavior for Database Management:

Check for Database Existence: The ORM first checks whether the specified database already exists.

Database Connection:

If the database exists:
  The ORM establishes a connection to the existing database.
If the database does not exist:
  The ORM creates the required database and then establishes the connection.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

from src.database.schema.city import Base

USER = "pg-2"
PASSWORD = "pg-2"
HOST = "postgres"
PORT = "5432"
DB_NAME = "navigation"

engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/postgres"
)

with engine.connect() as connection:
    try:
        result = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": DB_NAME},
        )
        exists = result.fetchone() is not None

        if not exists:
            connection.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"Database '{DB_NAME}' created.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

    except ProgrammingError as e:
        print(f"Error: {e}")
        raise

new_engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
)

with new_engine.connect() as new_connection:
    try:
        Base.metadata.create_all(new_engine)
        print("Tables created")
    except ProgrammingError as e:
        print(f"Error creating tables: {e}")
