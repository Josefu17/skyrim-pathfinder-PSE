"""This module calculates the route between two endpoints"""

import heapq
import math
from collections import defaultdict

from backend.src.logging_config import get_logging_configuration

logger = get_logging_configuration()


def get_route(start_city_name, end_city_name, data):
    """Calculates the route and returns the results."""
    logger.info("Calculating route from %s to %s.", start_city_name, end_city_name)
    cities = data["cities"]

    end_city, start_city = find_start_and_end_cities(
        cities, end_city_name, start_city_name
    )

    if not start_city or not end_city:
        logger.error(
            "One of the cities was not found: %s, %s.", start_city_name, end_city_name
        )
        return {
            "error": f"One of the cities was not found: {start_city_name}, {end_city_name}"
        }

    graph = create_graph(data)
    try:
        path, distance, second_path, second_distance = dijkstra(
            graph, start_city["id"], end_city["id"]
        )
        if distance == float("inf"):
            logger.warning(
                "No connection found between %s and %s.", start_city_name, end_city_name
            )
            return {
                "error": f"No connection found between {start_city_name} and {end_city_name}"
            }

        # Convert paths to city names
        path_names = {
            str(index): get_city_by_id(cities, city_id)["name"]
            for index, city_id in enumerate(path)
        }
        second_path_names = {}
        if second_path:
            second_path_names = {
                str(index): get_city_by_id(cities, city_id)["name"]
                for index, city_id in enumerate(second_path)
            }

        result = {
            "route": path_names,
            "distance": round(distance, 2),
            "alternative_route": second_path_names,
            "alternative_distance": round(second_distance, 2),
        }

        logger.info(
            "Route calculated successfully from %s to %s.",
            start_city_name,
            end_city_name,
        )
        return result

    except KeyError as e:
        logger.error("Error during route calculation: Missing key %s.", e)
        return {"error": f"Error during route calculation: Missing key {e}"}
    except ValueError as e:
        logger.error("Error during route calculation: Invalid value %s.", e)
        return {"error": f"Error during route calculation: {e}"}


def create_graph(data):
    """add all connections for each city"""
    logger.debug("Creating graph from map data.")
    graph = defaultdict(list)

    connections = data["connections"]
    cities = data["cities"]

    for connection in connections:
        city_1 = get_city_by_id(cities, connection["parent_city_id"])
        city_2 = get_city_by_id(cities, connection["child_city_id"])

        if not city_1 or not city_2:
            logger.warning("Connection skipped due to missing city: %s.", connection)
            continue

        distance = calculate_distance(city_1, city_2)

        graph[city_1["id"]].append((distance, city_2["id"]))
        graph[city_2["id"]].append((distance, city_1["id"]))

    logger.debug("Graph created successfully.")
    return graph


def dijkstra(graph, start_city_id, end_city_id):
    """Calculates the shortest and second-shortest routes."""
    logger.info(
        "Calculating shortest and second shortest routes from city %s to city %s.",
        start_city_id,
        end_city_id,
    )

    if start_city_id == end_city_id:
        return [start_city_id], 0, [start_city_id], 0

    min_heap = [(0, start_city_id, [])]  # Priority queue
    distances = {city_id: float("inf") for city_id in graph}
    distances[start_city_id] = 0
    second_distances = {city_id: float("inf") for city_id in graph}
    path = []
    second_path = []

    while min_heap:
        current_distance, current_city, current_path = heapq.heappop(min_heap)
        current_path = current_path + [current_city]

        if current_city == end_city_id:
            if not path:
                path = current_path
            elif not second_path:
                second_path = current_path
                break

        # Explore neighbors of the current city
        for distance, neighbor in graph[current_city]:
            new_distance = current_distance + distance

            # Update the shortest path
            if new_distance < distances[neighbor]:
                second_distances[neighbor] = distances[neighbor]  # Save old distance
                distances[neighbor] = new_distance
                heapq.heappush(min_heap, (new_distance, neighbor, current_path))
            # Update second-shortest path
            elif distances[neighbor] < new_distance < second_distances[neighbor]:
                second_distances[neighbor] = new_distance
                heapq.heappush(min_heap, (new_distance, neighbor, current_path))

    # Check if paths were found
    if not path or distances[end_city_id] == float("inf"):
        logger.warning(
            "No connection found between %s and %s.", start_city_id, end_city_id
        )
        return [], float("inf"), [], float("inf")

    if not second_path or second_distances[end_city_id] == float("inf"):
        logger.warning(
            "No alternative route found between %s and %s.", start_city_id, end_city_id
        )
        second_path = []

    return path, distances[end_city_id], second_path, second_distances[end_city_id]


def calculate_distance(city_1, city_2):
    """calculates the distance between cities"""
    distance = math.sqrt(
        (city_1["position_x"] - city_2["position_x"]) ** 2
        + (city_1["position_y"] - city_2["position_y"]) ** 2
    )
    logger.debug(
        "Distance between %s and %s: %s.", city_1["name"], city_2["name"], distance
    )
    return distance


def find_start_and_end_cities(cities, end_city_name, start_city_name):
    """finds the start and end cities with matching name from list of dicts"""
    start_city, end_city = None, None

    for city in cities:
        if city["name"] == start_city_name:
            start_city = city
        elif city["name"] == end_city_name:
            end_city = city
        if start_city and end_city:
            break
    logger.info("Start and end cities found.")
    return end_city, start_city


def get_city_by_id(cities, city_id):
    """returns the city dictionary with the given id in cities"""
    for city in cities:
        if city["id"] == city_id:
            return city
    logger.warning("City with %s not found", city_id)
    return None
