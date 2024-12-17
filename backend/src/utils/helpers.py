"""Python file for general-purpose helper functions"""

import logging
import os

from dotenv import load_dotenv


def get_logging_configuration():
    """return project-wide default logging configuration"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)


logger = get_logging_configuration()


def load_dotenv_if_exists(path):
    """Helper to load the environment variables in the given path if it exists"""
    if os.path.exists(path):
        load_dotenv(path)
        logger.info("Loaded .env from %s", path)
    else:
        logger.warning(
            ".env file not found at %s; ensure environment variables are set manually",
            path,
        )
