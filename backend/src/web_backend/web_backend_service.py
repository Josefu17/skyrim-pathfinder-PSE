"""Service for web backend, works with backend controller."""

import xmlrpc.client

from backend.src.database.dao.city_dao import CityDAO
from backend.src.database.dao.connection_dao import ConnectionDAO
from backend.src.logging_config import get_logging_configuration

logger = get_logging_configuration()


def fetch_route_from_navigation_service(start_city_name, end_city_name, session):
    """Fetch the shortest route from the navigation service by providing 2 cities"""
    try:

        with xmlrpc.client.ServerProxy("http://navigation-service:8000/") as proxy:
            cities, connections = (
                CityDAO.get_all_cities(session),
                ConnectionDAO.get_all_connections(session),
            )

            # convert objects to dicts to work with RPC-API
            cities_data = [city.to_dict() for city in cities]
            connections_data = [
                {
                    "parent_city_id": conn.parent_city_id,
                    "child_city_id": conn.child_city_id,
                }
                for conn in connections
            ]

            data = {
                "cities": cities_data,
                "connections": connections_data,
            }

            result = proxy.get_route(start_city_name, end_city_name, data)

            if result:
                logger.info(
                    "Route fetched successfully from %s and %s.",
                    start_city_name,
                    end_city_name,
                )
                return result
            logger.error(
                "Error calculating route from %s to %s.", start_city_name, end_city_name
            )
            return {"error": "Error by Route Calculation"}

    except xmlrpc.client.Error as e:
        logger.error("XML-RPC error: %s", e)
        return f"XML-RPC error: {e}"
    except ConnectionError as e:
        logger.error("Connection error: %s", e)
        return f"Connection error: {e}"


def fetch_cities_as_dicts(session):
    """Retrieve and return cities information from the database as dictionary"""
    # Fetch all cities as objects
    cities = CityDAO.get_all_cities(session)
    # Convert each city to a dictionary, excluding the 'id' field
    cities_data = [
        {
            "name": city.name,
            "position_x": city.position_x,
            "position_y": city.position_y,
        }
        for city in cities
    ]
    return cities_data


def service_get_map_data(session):
    """Fetch map data for controller"""
    cities = CityDAO.get_all_cities(session)
    connections = ConnectionDAO.get_all_connections(session)

    cities_data = [city.to_dict() for city in cities]
    connections_data = [
        {"parent_city_id": conn.parent_city_id, "child_city_id": conn.child_city_id}
        for conn in connections
    ]
    return cities_data, connections_data


def service_get_cities_data(session):
    """Fetch cities data for controller"""
    cities = CityDAO.get_all_cities(session)
    return [
        {
            "name": city.name,
            "position_x": city.position_x,
            "position_y": city.position_y,
        }
        for city in cities
    ]
