"""handles connection sessions to the database"""

import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.src.logging_config import get_logging_configuration

logger = get_logging_configuration()

# getcwd(): path where the script was executed
dotenv_path = os.path.join(os.getcwd(), ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    logger.info("Loaded .env from %s", dotenv_path)
else:
    logger.warning(
        ".env file not found at %s; ensure environment variables are set manually",
        dotenv_path,
    )


class DatabaseConnection:
    """Database connection class"""

    def __init__(self, config=None):
        """Initialize a database connection with specified parameters or fallback to environment"""
        env_config = {
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "database": os.getenv("DB_DATABASE"),
        }

        final_config = update_config_with_parameter_values(config, env_config)
        logger.debug("Final config: %s", final_config)

        # Assign final values to instance variables
        self.user = final_config["user"]
        self.password = final_config["password"]
        self.host = final_config["host"]
        self.port = final_config["port"]
        self.database = final_config["database"]

        self._check_missing_parameters()

        # Create the engine and session maker
        self.engine = create_engine(
            f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:"
            f"{self.port}/{self.database}"
        )
        self.session_local = sessionmaker(bind=self.engine)

    def _check_missing_parameters(self):
        """Helper method to check and raise an error if any parameters are missing"""
        params = {
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "database": self.database,
        }
        missing_params = [param for param, value in params.items() if value is None]
        if missing_params:
            raise ValueError(
                f"Database connection parameters not set properly. "
                f"Missing: {', '.join(missing_params)}"
            )

    def get_engine(self):
        """Get the database engine"""
        logger.debug("Getting database engine")
        return self.engine

    def get_session_local(self) -> sessionmaker:
        """Get the session maker"""
        logger.debug("Getting session maker")
        return self.session_local


@contextmanager
def get_db_session(config=None) -> Session:
    """Getter for DB session with the configured parameters"""
    db_connection = DatabaseConnection(config)
    session_local = db_connection.get_session_local()
    db = session_local()
    logger.debug("Database session opened")
    try:
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")


def update_config_with_parameter_values(config, env_config):
    """overwrite default db_credentials with given parameters (if any)"""
    # Initialize final_config with values from env_config
    final_config = env_config.copy()

    if config:
        for key in config:
            if config[key] is not None:  # Only overwrite if the value in config is not None
                final_config[key] = config[key]
    return final_config
