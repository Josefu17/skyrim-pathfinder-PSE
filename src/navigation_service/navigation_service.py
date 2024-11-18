"""This module calculates the route between two endpoints"""

import heapq
import math
from collections import defaultdict


def get_route(start_city_name, end_city_name, data):
    """calculates the shortest route and returns a dict containing the route as well as the
    total distance"""
    start_city, end_city = None, None
    cities = data["cities"]

    # Find start and end cities
    for city in cities:
        if city["name"] == start_city_name:
            start_city = city
        elif city["name"] == end_city_name:
            end_city = city
        if start_city and end_city:
            break

    if not start_city or not end_city:
        return {
            "error": f"One of the cities not found: {start_city_name}, {end_city_name}"
        }

    graph = create_graph(data)
    try:
        path, distance = dijkstra(graph, start_city["id"], end_city["id"])
        if distance == float("inf"):
            return {
                "error": f"No connection between {start_city_name} and {end_city_name}"
            }

        path_names = {
            str(index): get_city_by_id(cities, city_id)["name"]
            for index, city_id in enumerate(path)
        }
        result = {"route": path_names, "distance": round(distance, 2)}

        return result

    except KeyError as e:
        return {"error": f"Error by route calculation: Missing key {e}"}
    except ValueError as e:
        return {"error": f"Error by route calculation: {e}"}


def create_graph(data):
    """add all connections for each city"""
    graph = defaultdict(list)

    connections = data["connections"]
    cities = data["cities"]

    for connection in connections:
        city_1 = get_city_by_id(cities, connection["parent_city_id"])
        city_2 = get_city_by_id(cities, connection["child_city_id"])

        if not city_1 or not city_2:
            continue

        distance = calculate_distance(city_1, city_2)

        graph[city_1["id"]].append((distance, city_2["id"]))
        graph[city_2["id"]].append((distance, city_1["id"]))

    return graph


def dijkstra(graph, start_city_id, end_city_id):
    """calculates the shortest route"""

    min_heap = [(0, start_city_id)]
    distances = {city_id: float("inf") for city_id in graph}
    distances[start_city_id] = 0
    previous_nodes = {city_id: None for city_id in graph}

    while min_heap:
        current_distance, current_city = heapq.heappop(min_heap)

        if current_city == end_city_id:
            break

        for distance, neighbor in graph[current_city]:
            new_distance = current_distance + distance

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_city
                heapq.heappush(min_heap, (new_distance, neighbor))

    path = []
    city = end_city_id
    while city is not None:
        path.append(city)
        city = previous_nodes[city]
    path = path[::-1]

    return path, distances[end_city_id]


def calculate_distance(city_1, city_2):
    """calculates the distance between cities"""
    return math.sqrt(
        (city_1["position_x"] - city_2["position_x"]) ** 2
        + (city_1["position_y"] - city_2["position_y"]) ** 2
    )


def get_city_by_id(cities, city_id):
    """returns the city dictionary with the given id in cities"""
    for city in cities:
        if city["id"] == city_id:
            return city
    return None
