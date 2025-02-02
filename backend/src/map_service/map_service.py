"""map service to retrieve map information from the provided external map service"""

import requests
from sqlalchemy.orm import Session

from backend.src.database.dao.city_dao import CityDao
from backend.src.database.dao.connection_dao import ConnectionDao
from backend.src.database.dao.map_dao import MapDao
from backend.src.database.schema.city import City
from backend.src.database.schema.connection import Connection
from backend.src.database.schema.map import Map
from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


def get_maps_from_service():
    """Fetch map data from the map service."""
    map_url = "https://maps.proxy.devops-pse.users.h-da.cloud/maps"
    try:
        logger.info("Fetching map data.")
        response = requests.get(map_url, timeout=10)
        response.raise_for_status()
        logger.info("Map data fetched successfully.")
        return list(response.json())
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching map data: %s", e)
        return []


def fetch_and_store_map_data_if_needed(session: Session):
    """Fetch data from service and save in the database if needed."""
    map_list = get_maps_from_service()

    for map_name in map_list:
        logger.info("Processing map: %s", map_name)

        map_info = MapDao.get_map_by_name(session, map_name)
        if map_info:
            logger.info(
                "Map %s already exists in the database. Skipping further processing.", map_name
            )
            continue

        if map_name == "50000":
            logger.info("Map %s is too large to process. Skipping further processing.", map_name)
            continue

        map_url = f"https://maps.proxy.devops-pse.users.h-da.cloud/map?name={map_name}"

        try:
            logger.info("Fetching map data.")
            response = requests.get(map_url, timeout=60)
            response.raise_for_status()
            logger.info("Map data fetched successfully.")

            data = response.json()

            # Create a new map entry
            map_info = Map(
                name=map_name,
                size_x=data["mapsizeX"],
                size_y=data["mapsizeY"],
            )
            map_info = MapDao.save_map(map_info, session)
            logger.info("Map %s saved successfully", map_info.name)

            # Process cities in bulk
            cities_to_insert = [
                City(
                    map_id=map_info.id,
                    name=city["name"],
                    position_x=city["positionX"],
                    position_y=city["positionY"],
                )
                for city in data["cities"]
                if not CityDao.get_city_by_name(map_info.id, city["name"], session)
            ]
            if cities_to_insert:
                CityDao.save_cities_bulk(cities_to_insert, session)
                logger.info("Inserted %s cities for map %s.", len(cities_to_insert), map_name)

            # Create a mapping of city names to IDs
            city_map = {
                city["name"]: existing_city.id
                for city in data["cities"]
                if (existing_city := CityDao.get_city_by_name(map_info.id, city["name"], session))
            }

            # Process connections in bulk
            new_connections = [
                Connection(
                    map_id=map_info.id,
                    parent_city_id=city_map[connection["parent"]],
                    child_city_id=city_map[connection["child"]],
                )
                for connection in data["connections"]
                if city_map.get(connection["parent"])
                and city_map.get(connection["child"])
                and not ConnectionDao.get_connection_by_parent_and_child(
                    map_id=map_info.id,
                    parent_city_id=city_map[connection["parent"]],
                    child_city_id=city_map[connection["child"]],
                    session=session,
                )
            ]
            if new_connections:
                ConnectionDao.save_connections_bulk(new_connections, session)
                logger.info("Inserted %s connections for map %s.", len(new_connections), map_name)

        except requests.exceptions.RequestException as e:
            logger.error("Error fetching map data: %s", e)

    logger.info("All maps fetched and stored successfully.")
