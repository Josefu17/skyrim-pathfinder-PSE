"""
GRAPH FORMAT
1: [(1, 2), (4, 3)],
city_1: [(distance_to_city_2, city_2), (distance_to_city_3, city_3)]
"""

from backend.src.navigation_service.navigation_service import dijkstra


def test_dijkstra_connected_graph():
    """shortest path in a connected graph"""
    graph = fabricate_graph()
    path, distance = dijkstra(graph, 1, 4)
    assert path == [1, 2, 3, 4]
    assert distance == 6


def test_dijkstra_same_start_end():
    """same start and destination"""
    graph = fabricate_graph()
    path, distance = dijkstra(graph, 1, 1)
    assert path == [1]
    assert distance == 0


def test_dijkstra_disconnected_graph():
    """not connected endpoints"""
    disconnected_graph = {1: [(1, 2)], 2: [], 3: []}
    path, distance = dijkstra(disconnected_graph, 1, 3)
    assert path == [3]
    assert distance == float("inf")


def fabricate_graph():
    """Fabricate a graph for test purposes"""
    return {
        1: [(1, 2), (4, 3)],
        2: [(1, 1), (2, 3), (6, 4)],
        3: [(4, 1), (2, 2), (3, 4)],
        4: [(6, 2), (3, 3)],
    }
