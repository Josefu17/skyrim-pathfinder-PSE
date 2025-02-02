"""Unit tests for helpers.py"""

from unittest.mock import patch, MagicMock
import pytest
from backend.src.utils.helpers import (
    MetricsLogger,
    load_dotenv_if_exists,
)


@pytest.fixture
def redis_client():
    """Fixture to create a mock Redis client"""
    return MagicMock()


@pytest.fixture
def mock_metrics_logger(redis_client):
    """Fixture to create a MetricsLogger instance with a mock Redis client"""
    return MetricsLogger(redis_client)


def test_incr(mock_metrics_logger):
    """Test the incr method of MetricsLogger"""
    mock_metrics_logger.incr("test_metric")
    mock_metrics_logger.redis_client.incrby.assert_called_once_with("test_metric", 1)


def test_decr(mock_metrics_logger):
    """Test the decr method of MetricsLogger"""
    mock_metrics_logger.decr("test_metric")
    mock_metrics_logger.redis_client.decr.assert_called_once_with("test_metric", 1)


def test_set(mock_metrics_logger):
    """Test the set method of MetricsLogger"""
    mock_metrics_logger.set("test_metric", 100)
    mock_metrics_logger.redis_client.set.assert_called_once_with("test_metric", 100)


def test_incr_by_float(mock_metrics_logger):
    """Test the incr_by_float method of MetricsLogger"""
    mock_metrics_logger.incr_by_float("test_metric", 1.5)
    mock_metrics_logger.redis_client.incrbyfloat.assert_called_once_with("test_metric", 1.5)


def test_get(mock_metrics_logger):
    """Test the get method of MetricsLogger"""
    mock_metrics_logger.redis_client.get.return_value = b"100"
    value = mock_metrics_logger.get("test_metric")
    assert value == 100
    mock_metrics_logger.redis_client.get.assert_called_once_with("test_metric")


@patch("backend.src.utils.helpers.os.path.exists")
@patch("backend.src.utils.helpers.load_dotenv")
def test_load_dotenv_if_exists(mock_load_dotenv, mock_exists):
    """Test the load_dotenv_if_exists function"""
    mock_exists.return_value = True
    load_dotenv_if_exists(".env")
    mock_load_dotenv.assert_called_once_with(".env")
