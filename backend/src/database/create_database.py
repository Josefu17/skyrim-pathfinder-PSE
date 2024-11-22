"""
ORM Behavior for Database Management:

Check for Database Existence: The ORM first checks whether the specified database already exists.

Database Connection:

If the database exists:
  The ORM establishes a connection to the existing database.
If the database does not exist:
  The ORM creates the required database and then establishes the connection.
"""

from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

from backend.src.database.db_connection import DatabaseConnection
from backend.src.database.schema.base import Base
from backend.src.database.schema import models
from backend.src.logging_config import get_logging_configuration

logger = get_logging_configuration()

# Ensure db models are registered
models.register_models()

# Step 1: Connect to the 'postgres' database to check for and create 'navigation' if needed
postgres_connection = DatabaseConnection(config={"database": "postgres"})
postgres_engine = postgres_connection.get_engine()

NAVIGATION_DB_NAME = "navigation"

with postgres_engine.connect() as connection:
    try:
        # Set isolation level to AUTOCOMMIT to create a database outside a transaction
        connection.execution_options(isolation_level="AUTOCOMMIT")
        result = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": NAVIGATION_DB_NAME},
        )
        exists = result.fetchone() is not None

        if not exists:
            connection.execute(text(f"CREATE DATABASE {NAVIGATION_DB_NAME}"))
            logger.info("Database '%s' created successfully.", NAVIGATION_DB_NAME)
        else:
            logger.info("Database '%s' already exists.", NAVIGATION_DB_NAME)
    except ProgrammingError as e:
        logger.error("Error: %s", e)
        raise

# Step 2: Connect to the 'navigation' database and create the tables
navigation_connection = DatabaseConnection(config={"database": NAVIGATION_DB_NAME})
navigation_engine = navigation_connection.get_engine()

with navigation_engine.connect() as new_connection:
    try:
        Base.metadata.create_all(navigation_engine)
        logger.info("Registered tables: %s", Base.metadata.tables.keys())
    except ProgrammingError as e:
        logger.error("Error creating tables: %s", e)
