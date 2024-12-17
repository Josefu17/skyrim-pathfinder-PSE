"""Fetches data from map service and saves the data to a relational database"""

import requests

from backend.src.database.dao.city_dao import CityDao
from backend.src.database.dao.connection_dao import ConnectionDao
from backend.src.database.schema.city import City
from backend.src.database.schema.connection import Connection
from backend.src.utils.helpers import get_logging_configuration
from backend.src.database.dao.map_dao import MapDao
from backend.src.database.schema.map import Map

logger = get_logging_configuration()

MAP_URL = "https://maps.proxy.devops-pse.users.h-da.cloud/map?name=skyrim"


def fetch_and_store_map_data_if_needed(session):
    """fetch data from service and save in database if needed"""
    try:
        logger.info("Fetching map data.")

        response = requests.get(MAP_URL, timeout=10)
        response.raise_for_status()

        logger.info("Map data fetched successfully.")

        data = response.json()

        map_info = MapDao.get_map(session)
        if not map_info:
            map_info = Map(
                name=data["mapname"],
                size_x=data["mapsizeX"],
                size_y=data["mapsizeY"],
            )
            MapDao.save_map(map_info, session)
        city_map = {}

        for city in data["cities"]:
            db_city = CityDao.get_city_by_name(city["name"], session)
            if not db_city:
                db_city = City(
                    name=city["name"],
                    position_x=city["positionX"],
                    position_y=city["positionY"],
                )
                CityDao.save_city(db_city, session)
                logger.info("City %s saved", city["name"])
            city_map[city["name"]] = db_city.id

        new_connections = []

        for connection in data["connections"]:
            parent_city_id = city_map.get(connection["parent"])
            child_city_id = city_map.get(connection["child"])

            if parent_city_id and child_city_id:
                db_connection = ConnectionDao.get_connection_by_parent_and_child(
                    parent_city_id=parent_city_id,
                    child_city_id=child_city_id,
                    session=session,
                )
                if not db_connection:
                    db_connection = Connection(
                        parent_city_id=parent_city_id, child_city_id=child_city_id
                    )
                    new_connections.append(db_connection)
                    logger.info(
                        "New Connection found from: %s to: %s",
                        parent_city_id,
                        child_city_id,
                    )

        if new_connections:
            ConnectionDao.save_connections_bulk(new_connections, session)
            logger.info("New Connections saved successfully")
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching map data: %s", e)
