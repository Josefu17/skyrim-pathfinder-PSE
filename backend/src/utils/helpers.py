"""Python file for general-purpose helper functions"""

import logging
import os
from datetime import datetime
import redis
from dotenv import load_dotenv

redis_instance = redis.StrictRedis(host="redis", port=6379, db=0)


class MetricsLogger:
    """Class to log metrics to Redis and log files."""

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def _get_formatted_time(self):
        """Return the current time in a formatted string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def incr(self, key, amount=1):
        """Increment a metric in Redis and log the change."""
        self.redis_client.incrby(key, amount)
        logger.info(
            {"metric": key, "value": self.get(key), "timestamp": self._get_formatted_time()},
        )

    def log_execution_time(self, key, amount):
        """Log the execution time of a function."""
        self.redis_client.incrbyfloat(key, amount)

    def decr(self, key, amount=1):
        """Decrement a metric in Redis and log the change."""
        self.redis_client.decr(key, amount)
        logger.info(
            {"metric": key, "value": self.get(key), "timestamp": self._get_formatted_time()},
        )

    def set(self, key, value):
        """Set a metric in Redis and log the change."""
        self.redis_client.set(key, value)
        logger.info({"metric": key, "value": value, "timestamp": self._get_formatted_time()})

    def log_calculated_route_for_user(self, user_id, key_prefix):
        """Log the calculated route for a user."""
        logger.info(
            {
                "user_id": user_id,
                "timestamp": self._get_formatted_time(),
                "calculated_route": f"m_{key_prefix}_calculated",
                "calculation_time": self.get(f"m_{key_prefix}_execution_time"),
            }
        )

    def get(self, key):
        """Get a metric from Redis and log the change."""
        value = self.redis_client.get(key)
        logger.info(
            {"metric": key, "value": value, "timestamp": self._get_formatted_time()},
        )

        if value:
            try:
                return float(value)
            except ValueError:
                try:
                    return int(value)
                except ValueError:
                    return value
        return 0

    def incrbyfloat(self, key, amount):
        """Increment a metric by a float value in Redis and log the change."""
        self.redis_client.incrbyfloat(key, amount)

        total_time = self.get(key) or 0
        total_count = self.get(f"m_{key}_calculation_count") or 1

        logger.info("total time: %s", total_time)
        logger.info("total count: %s", total_count)

        avg_time = total_time / total_count

        metric_name = f"m_{key}_execution_time_avg"
        self.redis_client.set(metric_name, avg_time)
        logger.info(
            {
                "metric": metric_name,
                "value": self.get(metric_name),
                "timestamp": self._get_formatted_time(),
            },
        )


def get_logging_configuration():
    """Set up logging configuration"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)


logger = get_logging_configuration()


def load_dotenv_if_exists(path):
    """Load .env file if it exists"""
    if os.path.exists(path):
        load_dotenv(path)
        logger.info("Loaded .env file", extra={"path": path, "timestamp": datetime.now()})
    else:
        logger.warning(".env file not found", extra={"path": path, "timestamp": datetime.now()})


metrics_logger = MetricsLogger(redis_instance)
