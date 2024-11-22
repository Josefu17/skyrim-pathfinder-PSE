"""handles connection sessions to the database"""

from contextlib import contextmanager
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Load environment variables from the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "../../env/.env")
load_dotenv(dotenv_path)


class DatabaseConnection:
    """Database connection class"""

    def __init__(self, config=None):
        """Initialize a database connection with specified parameters or fallback to environment"""
        if config is None:
            config = {
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
                "host": os.getenv("DB_HOST"),
                "port": os.getenv("DB_PORT"),
                "database": os.getenv("DB_DATABASE"),
            }
        # Use the provided values or fallback to environment variables
        self.user = config.get("user") or os.getenv("DB_USER")
        self.password = config.get("password") or os.getenv("DB_PASSWORD")
        self.host = config.get("host") or os.getenv("DB_HOST")
        self.port = config.get("port") or os.getenv("DB_PORT")
        self.database = config.get("database") or os.getenv("DB_DATABASE")

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
        return self.engine

    def get_session_local(self) -> sessionmaker:
        """Get the session maker"""
        return self.session_local


@contextmanager
def get_db_session(config=None) -> Session:
    """Getter for DB session with the configured parameters"""
    db_connection = DatabaseConnection(config)
    session_local = db_connection.get_session_local()
    db = session_local()
    try:
        yield db
    finally:
        db.close()
