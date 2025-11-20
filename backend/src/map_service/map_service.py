"""map service to retrieve map information from the provided external map service"""
from random import Random

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

# MAP_SERVICE_URL = "https://maps.proxy.devops-pse.users.h-da.cloud"

DUMMY_MAP_SIZES = [10, 25, 50, 100]


def _generate_dummy_map_data():
    """
    Generate deterministic dummy map definitions.

    Returns a list of dicts with the same shape as the old external map JSON:
    {
        "name": "...",
        "mapsizeX": int,
        "mapsizeY": int,
        "cities": [
            {"name": str, "positionX": int, "positionY": int},
            ...
        ],
        "connections": [
            {"parent": city_name, "child": city_name},
            ...
        ],
    }
    """
    rng = Random(42)  # deterministic for reproducibility
    dummy_maps = []

    for size in DUMMY_MAP_SIZES:
        map_name = f"Dummy-{size}x{size}"
        cities = []

        # Generate `size` cities inside the [0, size_x-1] / [0, size_y-1] bounds
        for i in range(size):
            # keep it simple but spread a bit over the map
            x = rng.randint(0, size - 1)
            y = rng.randint(0, size - 1)
            cities.append(
                {
                    "name": f"City_{size}_{i + 1}",
                    "positionX": x,
                    "positionY": y,
                }
            )

        # Simple chain connections to ensure the graph is connected:
        # City_1 -> City_2 -> ... -> City_N
        connections = []
        for i in range(len(cities) - 1):
            connections.append(
                {
                    "parent": cities[i]["name"],
                    "child": cities[i + 1]["name"],
                }
            )

        dummy_maps.append(
            {
                "name": map_name,
                "mapsizeX": size,
                "mapsizeY": size,
                "cities": cities,
                "connections": connections,
            }
        )

    return dummy_maps


# Not used anymore since the map provider endpoint was a university-internal one, yb

# def get_maps_from_service():
#     """Fetch map data from the map service."""
#     with tracer.start_as_current_span("fetch_map_data_external") as span:
#         map_url = f"{MAP_SERVICE_URL}/maps"
#         try:
#             logger.info("Fetching maps list.")
#             response = requests.get(map_url, timeout=10)
#             response.raise_for_status()
#             span.set_attribute("http.status_code", response.status_code)
#
#             logger.info("Maps list fetched successfully.")
#             return list(response.json())
#         except requests.exceptions.RequestException as e:
#             logger.error("Error fetching map data: %s", e)
#             return []

def fetch_and_store_map_data_if_needed(session: Session):
    """
    Check if maps already exist in the database.
    - If yes: do nothing.
    - If no: generate dummy maps (10x10, 25x25, 50x50, 100x100),
      create cities & connections and store them.
    """
    with tracer.start_as_current_span("check_existing_maps") as span:
        existing_maps = MapDao.get_all_maps(session) if hasattr(MapDao, "get_all_maps") else None

        if existing_maps is None:
            # Fallback if there is no DAO helper – query directly
            existing_count = session.query(Map).count()
        else:
            existing_count = len(existing_maps)

        if existing_count > 0:
            logger.info("Maps already present in DB (%s). Skipping dummy generation.", existing_count)
            return

        logger.info("No maps found in DB. Generating dummy maps.")
        span.set_attribute("maps_generated", True)

    dummy_maps = _generate_dummy_map_data()

    with tracer.start_as_current_span("process_dummy_map_data") as span:
        try:
            for dummy in dummy_maps:
                map_name = dummy["name"]
                logger.info("Creating dummy map: %s", map_name)

                # Double-check by name in case of race conditions
                if MapDao.get_map_by_name(session, map_name):
                    logger.info("Map %s already exists. Skipping.", map_name)
                    continue

                # Create map entry
                new_map = Map(
                    name=map_name,
                    size_x=dummy["mapsizeX"],
                    size_y=dummy["mapsizeY"],
                )
                new_map = MapDao.save_map(new_map, session)
                logger.info("Map %s saved successfully (id=%s).", new_map.name, new_map.id)

                # Insert cities
                cities_to_insert = [
                    City(
                        map_id=new_map.id,
                        name=city["name"],
                        position_x=city["positionX"],
                        position_y=city["positionY"],
                    )
                    for city in dummy["cities"]
                ]

                if cities_to_insert:
                    CityDao.save_cities_bulk(cities_to_insert, session)
                    logger.info("Inserted %s cities for map %s.", len(cities_to_insert), map_name)
                inserted_cities = CityDao.get_cities_by_map_id(new_map.id, session)
                city_map = {city.name: city.id for city in inserted_cities}

                # Insert connections (only if both endpoints exist)
                new_connections = [
                    Connection(
                        map_id=new_map.id,
                        parent_city_id=city_map[conn["parent"]],
                        child_city_id=city_map[conn["child"]],
                    )
                    for conn in dummy["connections"]
                    if conn["parent"] in city_map and conn["child"] in city_map
                ]

                if new_connections:
                    ConnectionDao.save_connections_bulk(new_connections, session)
                    logger.info(
                        "Inserted %s connections for map %s.",
                        len(new_connections),
                        map_name,
                    )

        except Exception as e:
            logger.error("Error while generating dummy maps: %s", e)
            set_span_error_flags(span, e)

    logger.info("Dummy maps generated and stored successfully.")


# Not used anymore since the map provider endpoint was a university-internal one, yb

# def fetch_and_store_map_data_if_needed(session: Session):
#     """
#     Check if maps already exist in the database.
#     - If yes: do nothing.
#     - If no: generate dummy maps (10x10, 25x25, 50x50, 100x100),
#       create cities & connections and store them.
#     """
#     map_list = get_maps_from_service()
#
#     with tracer.start_as_current_span("process_map_data") as span:
#         for map_name in map_list:
#             logger.info("Processing map: %s", map_name)
#
#             if MapDao.get_map_by_name(session, map_name):
#                 logger.info(
#                     logger.info("Map %s already exists in the database. Skipping.", map_name)
#                 )
#                 continue
#
#             map_url = f"{MAP_SERVICE_URL}/map?name={map_name}"
#
#             try:
#                 data = fetch_map_json(map_url)
#
#                 # Create a new map entry
#                 new_map = Map(
#                     name=map_name,
#                     size_x=data["mapsizeX"],
#                     size_y=data["mapsizeY"],
#                 )
#                 new_map = MapDao.save_map(new_map, session)
#                 logger.info("Map %s saved successfully", new_map.name)
#
#                 # Process cities in bulk
#                 cities_to_insert = [
#                     City(
#                         map_id=new_map.id,
#                         name=city["name"],
#                         position_x=city["positionX"],
#                         position_y=city["positionY"],
#                     )
#                     for city in data["cities"]
#                 ]
#                 if cities_to_insert:
#                     CityDao.save_cities_bulk(cities_to_insert, session)
#                     logger.info("Inserted %s cities for map %s.", len(cities_to_insert), map_name)
#
#                     inserted_cities = CityDao.get_cities_by_map_id(new_map.id, session)
#
#                     # Create a mapping of city names to IDs
#                     city_map = {city.name: city.id for city in inserted_cities}
#
#                     # Process connections in bulk
#                     new_connections = [
#                         Connection(
#                             map_id=new_map.id,
#                             parent_city_id=city_map[connection["parent"]],
#                             child_city_id=city_map[connection["child"]],
#                         )
#                         for connection in data["connections"]
#                         if connection["parent"] in city_map and connection["child"] in city_map
#                     ]
#                     if new_connections:
#                         ConnectionDao.save_connections_bulk(new_connections, session)
#                         logger.info(
#                             "Inserted %s connections for map %s.", len(new_connections), map_name
#                         )
#
#             except requests.exceptions.RequestException as e:
#                 logger.error("Error fetching map data: %s", e)
#                 set_span_error_flags(span, e)
#
#     logger.info("All maps fetched and stored successfully.")


def fetch_map_json(map_url):
    """fetch data for a specific map and return its JSON data."""
    logger.info("Fetching map data.")
    response = requests.get(map_url, timeout=60)
    response.raise_for_status()
    logger.info("Map data fetched successfully.")
    data = response.json()
    return data
