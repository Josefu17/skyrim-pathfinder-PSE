"""This module calculates the route between two endpoints"""

import math
from collections import defaultdict
import heapq
import json
from sqlalchemy.orm import sessionmaker
from database import new_engine, Cities, Connections


SESSIONMAKER = sessionmaker(bind=new_engine)
SESSION = SESSIONMAKER()


def calculate_distance(city_1, city_2):
    """calculates the distance between cities"""
    return math.sqrt(
        (city_1.position_x - city_2.position_x) ** 2
        + (city_1.position_y - city_2.position_y) ** 2
    )


def create_graph():
    """add all connections for each city"""
    graph = defaultdict(list)
    cities = {city.id: city for city in SESSION.query(Cities).all()}
    connections = SESSION.query(Connections).all()

    for connection in connections:
        city_1 = cities[connection.parent_city_id]
        city_2 = cities[connection.child_city_id]
        distance = calculate_distance(city_1, city_2)

        graph[city_1.id].append((distance, city_2.id))
        graph[city_2.id].append((distance, city_1.id))

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


def get_route(start_city_name, end_city_name):
    """displays the shortest route"""
    start_city = SESSION.query(Cities).filter_by(name=start_city_name).first()
    end_city = SESSION.query(Cities).filter_by(name=end_city_name).first()

    if not start_city or not end_city:
        return f"One of the cities not found: {start_city_name}, {end_city_name}"

    graph = create_graph()
    path, distance = dijkstra(graph, start_city.id, end_city.id)

    if distance == float("inf"):
        return f"No connection between {start_city_name} and {end_city_name}"

    path_names = [SESSION.query(Cities).get(city_id).name for city_id in path]
    route = {"route": " -> ".join(path_names), "distance": distance}
    return json.dumps(route)
