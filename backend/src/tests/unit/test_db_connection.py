"""Unit tests for database connection."""

from unittest.mock import patch, MagicMock

import pytest

from backend.src.database.db_connection import DatabaseConnection, get_db_session


# Test initializing DatabaseConnection with a complete config
def test_database_connection_full_config():
    """
    Test that the DatabaseConnection initializes correctly with a complete configuration dictionary.
    """
    config = {
        "user": "test_user",
        "password": "test_password",
        "host": "localhost",
        "port": "5432",
        "database": "test_db",
    }
    db_connection = DatabaseConnection(config)
    assert db_connection.user == "test_user"
    assert db_connection.password == "test_password"
    assert db_connection.host == "localhost"
    assert db_connection.port == "5432"
    assert db_connection.database == "test_db"


# Test fallback to environment variables
@patch.dict(
    "os.environ",
    {
        "DB_USER": "env_user",
        "DB_PASSWORD": "env_password",
        "DB_HOST": "env_host",
        "DB_PORT": "5432",
        "DB_DATABASE": "env_db",
    },
)
def test_database_connection_env_fallback():
    """
    Test that DatabaseConnection correctly falls back to environment variables
    when configuration is not explicitly provided.
    """
    db_connection = DatabaseConnection()
    assert db_connection.user == "env_user"
    assert db_connection.password == "env_password"
    assert db_connection.host == "env_host"
    assert db_connection.port == "5432"
    assert db_connection.database == "env_db"


# Test missing parameters (raises ValueError)
@patch.dict("os.environ", {}, clear=True)  # Clear environment variables to simulate missing values
def test_database_connection_missing_parameters():
    """
    Test that DatabaseConnection raises a ValueError when required parameters are missing,
    and environment variables are not set.
    """
    config = {
        "user": "test_user",
        "password": "test_password",
        "host": None,  # Simulate missing host
    }
    with pytest.raises(ValueError) as excinfo:
        DatabaseConnection(config)
    assert "host" in str(excinfo.value)


# Mocking create_engine to avoid real database connection
@patch("backend.src.database.db_connection.create_engine")
def test_database_connection_engine_creation(mock_create_engine):
    """
    Test that DatabaseConnection calls create_engine with the correct connection string,
    avoiding a real database connection by mocking create_engine.
    """
    config = {
        "user": "test_user",
        "password": "test_password",
        "host": "localhost",
        "port": "5432",
        "database": "test_db",
    }
    db_connection = DatabaseConnection(config)
    db_connection.get_engine()
    mock_create_engine.assert_called_once_with(
        "postgresql+psycopg2://test_user:test_password@localhost:5432/test_db"
    )


# Test the get_db_session context manager
@patch("backend.src.database.db_connection.DatabaseConnection.get_session_local")
@patch.dict(
    "os.environ",
    {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_DATABASE": "test_db",
    },
)
def test_get_db_session(mock_get_session_local):
    """
    Test that get_db_session context manager properly returns a session and closes it,
    using a mock for session creation.
    """
    mock_session = MagicMock()
    mock_get_session_local.return_value = MagicMock(return_value=mock_session)

    with get_db_session() as session:
        assert session == mock_session
    mock_session.close.assert_called_once()
