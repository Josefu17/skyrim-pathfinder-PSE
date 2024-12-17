"""
checks all criteria for the health status of the application
"""

import requests
from bs4 import BeautifulSoup
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from backend.src.database.db_connection import get_db_session
from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


def check_database_connection():
    """
    verify that database connection is healthy
    """
    try:
        with get_db_session() as session:
            result = session.execute(text("SELECT 1")).fetchone()
            if not result:
                logger.error("Health check: Database connection failed")
                return {
                    "database_connection": False,
                    "message": "Database connection failed",
                }
            logger.info("Database connection successful")
            return {"database_connection": True}
    except SQLAlchemyError as e:
        logger.error("Health check: Database connection failed with error: %s", str(e))
        return {"database_connection": False, "message": str(e)}


def check_map_service_connection():
    """
    verify that the connection to the map service is healthy
    """
    map_url = "https://maps.proxy.devops-pse.users.h-da.cloud/map?name=skyrim"
    try:
        response = requests.get(map_url, timeout=10)
        response.raise_for_status()
        if response.status_code == 200:
            logger.info("Connection to map service successful")
            return {"map_service_connection": True}
        logger.error("Request to map service failed")
        return {
            "map_service_connection": False,
            "message": "Request to map service failed",
        }
    except requests.exceptions.RequestException as e:
        logger.error("Health check: Map service connection failed with error: %s", str(e))
        return {"map_service_connection": False, "message": str(e)}


def check_navigation_service_connection():
    """
    verify that the connection to the navigation service is healthy
    """
    start_point = "Markarth"
    end_point = "Karthwasten"

    url = "http://localhost:4243/routes"
    data = {"startpoint": start_point, "endpoint": end_point}

    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        if response.status_code == 201:
            logger.info("Connection to navigation service successful")
            return {"navigation_service_connection": True}
        logger.error("Request to navigation service failed")
        return {
            "navigation_service_connection": False,
            "message": "Request to navigation service failed",
        }
    except requests.exceptions.RequestException as e:
        logger.error("Health check: Navigation service connection failed with error: %s", str(e))
        return {"navigation_service_connection": False, "message": str(e)}


def check_frontend_availability():
    """
    verify that the connection to the frontend is healthy
    """
    url = "http://web-frontend:80/"

    try:
        # send a GET request to the main page
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # error if HTTP status is not 200

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Check if the main elements are present
        required_elements = [
            {"tag": "div", "id": "root"},
        ]

        missing_elements = []

        all_present = True
        for element in required_elements:
            if element.get("text"):
                # Search for tag with specific text content
                found = soup.find(element["tag"], string=element["text"])
            elif element.get("id"):
                # Search for tag with a specific ID
                found = soup.find(element["tag"], id=element["id"])
            else:
                found = None

            if not found:
                logger.error("Missing: %s", str(element))
                missing_elements.append(element)
                all_present = False

        if all_present:
            logger.info("All elements are present!")
            return {"frontend_availability": True}

        logger.error("Some elements are missing!")
        return {
            "frontend_availability": False,
            "message": "Elements are missing",
            "missing_elements": missing_elements,
        }

    except requests.exceptions.RequestException as e:
        logger.error("Server check failed: %s", str(e))
        return {"frontend_availability": False, "message": str(e)}


def check_all_criteria():
    """
    Dictionary that contains all status for the health check
    """
    checks = {}
    checks.update(check_database_connection())
    checks.update(check_map_service_connection())
    checks.update(check_navigation_service_connection())
    checks.update(check_frontend_availability())
    return checks
