"""Logger configuration for reusability"""

# Configure simple logging
import logging


def get_logging_configuration():
    """return project-wide default logging configuration"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)
