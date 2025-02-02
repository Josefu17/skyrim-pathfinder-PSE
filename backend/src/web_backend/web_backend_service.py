"""Service for web backend, works with backend controller."""

import xmlrpc.client

from backend.src.database.dao.city_dao import CityDao
from backend.src.database.dao.connection_dao import ConnectionDao
from backend.src.database.dao.map_dao import MapDao
from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


def fetch_route_from_navigation_service(map_id, start_city_name, end_city_name, session):
    """Fetch the shortest route from the navigation service by providing two cities"""
    try:

        with xmlrpc.client.ServerProxy("http://navigation-service:8000/") as proxy:
            cities, connections = (
                CityDao.get_cities_by_map_id(map_id, session),
                ConnectionDao.get_connections_by_map_id(map_id, session),
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
                logger.info("Route fetched successfully between the two endpoints.")
                return result
            logger.error("Error occurred while calculation the route between endpoints.")
            return {"error": "Error during Route Calculation"}

    except xmlrpc.client.Error as e:
        logger.error("XML-RPC error: %s", e)
        return f"XML-RPC error: {e}"
    except ConnectionError as e:
        logger.error("Connection error: %s", e)
        return f"Connection error: {e}"


def fetch_cities_as_dicts(map_id, session):
    """Retrieve and return cities' information from the database as dictionary"""
    # Fetch all cities as objects
    cities = CityDao.get_cities_by_map_id(map_id, session)
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


def service_get_map_data(map_id, session):
    """Fetch map data for controller"""
    cities = CityDao.get_cities_by_map_id(map_id, session)
    connections = ConnectionDao.get_connections_by_map_id(map_id, session)
    map_info = MapDao.get_map_by_id(map_id, session)

    cities_data = [city.to_dict() for city in cities]
    connections_data = [
        {"parent_city_id": conn.parent_city_id, "child_city_id": conn.child_city_id}
        for conn in connections
    ]
    map_data = map_info.to_dict() if map_info else {}
    return map_data, cities_data, connections_data


def service_get_map_data_by_name(map_name, session):
    """Fetch map data for controller by map name"""
    map_info = MapDao.get_map_by_name(session, map_name)
    if not map_info:
        return None, None, None
    map_id = map_info.id
    cities = CityDao.get_cities_by_map_id(map_id, session)
    connections = ConnectionDao.get_connections_by_map_id(map_id, session)

    cities_data = [city.to_dict() for city in cities]
    connections_data = [
        {"parent_city_id": conn.parent_city_id, "child_city_id": conn.child_city_id}
        for conn in connections
    ]
    map_data = map_info.to_dict()
    return map_data, cities_data, connections_data


def service_get_cities_data(map_id, session):
    """Fetch cities data for controller"""
    cities = CityDao.get_cities_by_map_id(map_id, session)
    return [
        {
            "name": city.name,
            "position_x": city.position_x,
            "position_y": city.position_y,
        }
        for city in cities
    ]
