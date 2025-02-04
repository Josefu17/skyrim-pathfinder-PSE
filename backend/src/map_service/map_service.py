"""map service to retrieve map information from the provided external map service"""

import requests
from opentelemetry.trace import get_tracer
from sqlalchemy.orm import Session

from backend.src.database.dao.city_dao import CityDao
from backend.src.database.dao.connection_dao import ConnectionDao
from backend.src.database.dao.map_dao import MapDao
from backend.src.database.schema.city import City
from backend.src.database.schema.connection import Connection
from backend.src.database.schema.map import Map
from backend.src.utils.helpers import get_logging_configuration
from backend.src.utils.tracing import set_span_error_flags

logger = get_logging_configuration()
tracer = get_tracer("map-service")

MAP_SERVICE_URL = "https://maps.proxy.devops-pse.users.h-da.cloud"


def get_maps_from_service():
    """Fetch map data from the map service."""
    with tracer.start_as_current_span("fetch_map_data_external") as span:
        map_url = f"{MAP_SERVICE_URL}/maps"
        try:
            logger.info("Fetching maps list.")
            response = requests.get(map_url, timeout=10)
            response.raise_for_status()
            span.set_attribute("http.status_code", response.status_code)

            logger.info("Maps list fetched successfully.")
            return list(response.json())
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching map data: %s", e)
            return []


def fetch_and_store_map_data_if_needed(session: Session):
    """Fetch data from service and save in the database if needed."""
    map_list = get_maps_from_service()

    with tracer.start_as_current_span("process_map_data") as span:
        for map_name in map_list:
            logger.info("Processing map: %s", map_name)

            if MapDao.get_map_by_name(session, map_name):
                logger.info(
                    logger.info("Map %s already exists in the database. Skipping.", map_name)
                )
                continue

            map_url = f"{MAP_SERVICE_URL}/map?name={map_name}"

            try:
                data = fetch_map_json(map_url)

                # Create a new map entry
                new_map = Map(
                    name=map_name,
                    size_x=data["mapsizeX"],
                    size_y=data["mapsizeY"],
                )
                new_map = MapDao.save_map(new_map, session)
                logger.info("Map %s saved successfully", new_map.name)

                # Process cities in bulk
                cities_to_insert = [
                    City(
                        map_id=new_map.id,
                        name=city["name"],
                        position_x=city["positionX"],
                        position_y=city["positionY"],
                    )
                    for city in data["cities"]
                ]
                if cities_to_insert:
                    CityDao.save_cities_bulk(cities_to_insert, session)
                    logger.info("Inserted %s cities for map %s.", len(cities_to_insert), map_name)

                    inserted_cities = CityDao.get_cities_by_map_id(new_map.id, session)

                    # Create a mapping of city names to IDs
                    city_map = {city.name: city.id for city in inserted_cities}

                    # Process connections in bulk
                    new_connections = [
                        Connection(
                            map_id=new_map.id,
                            parent_city_id=city_map[connection["parent"]],
                            child_city_id=city_map[connection["child"]],
                        )
                        for connection in data["connections"]
                        if connection["parent"] in city_map and connection["child"] in city_map
                    ]
                    if new_connections:
                        ConnectionDao.save_connections_bulk(new_connections, session)
                        logger.info(
                            "Inserted %s connections for map %s.", len(new_connections), map_name
                        )

            except requests.exceptions.RequestException as e:
                logger.error("Error fetching map data: %s", e)
                set_span_error_flags(span, e)

    logger.info("All maps fetched and stored successfully.")


def fetch_map_json(map_url):
    """fetch data for a specific map and return its JSON data."""
    logger.info("Fetching map data.")
    response = requests.get(map_url, timeout=60)
    response.raise_for_status()
    logger.info("Map data fetched successfully.")
    data = response.json()
    return data
