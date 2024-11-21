"""Fetches data from map service and saves the data to a relational database"""

import requests

from src.database.db_connection import with_db_session
from src.database.dao.city_dao import CityDAO
from src.database.dao.connection_dao import ConnectionDAO
from src.database.schema.city import City
from src.database.schema.connection import Connection

MAP_URL = "https://maps.proxy.devops-pse.users.h-da.cloud/map?name=skyrim"


@with_db_session
def fetch_and_store_map_data_if_needed(session):
    """fetch data from service and save in database if needed"""
    try:
        response = requests.get(MAP_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        city_map = {}

        for city in data["cities"]:
            db_city = CityDAO.get_city_by_name(city["name"], session)
            if not db_city:
                db_city = City(
                    name=city["name"],
                    position_x=city["positionX"],
                    position_y=city["positionY"],
                )
                CityDAO.save_city(db_city, session)
                print(f"City {city['name']} added")
            city_map[city["name"]] = db_city.id

        new_connections = []

        for connection in data["connections"]:
            parent_city_id = city_map.get(connection["parent"])
            child_city_id = city_map.get(connection["child"])

            if parent_city_id and child_city_id:
                db_connection = ConnectionDAO.get_connection_by_parent_and_child(
                    parent_city_id=parent_city_id,
                    child_city_id=child_city_id,
                    session=session,
                )
                if not db_connection:
                    db_connection = Connection(
                        parent_city_id=parent_city_id, child_city_id=child_city_id
                    )
                    new_connections.append(db_connection)
                    print(
                        f"New Connection found from: {connection['parent']} "
                        f"to: {connection['child']}"
                    )

        if new_connections:
            ConnectionDAO.save_connections_bulk(new_connections, session)
            print("New Connections saved")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
