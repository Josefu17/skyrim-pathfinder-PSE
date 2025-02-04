"""
Tests get_route()
"""

from backend.src.navigation_service.navigation_service import get_route

data = {
    "cities": [
        {"id": 1, "name": "CityA"},
        {"id": 2, "name": "CityB"},
        {"id": 3, "name": "CityC"},
        {"id": 4, "name": "CityD"},
    ],
    "connections": [
        {"from": 1, "to": 2, "distance": 10},
        {"from": 2, "to": 3, "distance": 15},
        {"from": 1, "to": 3, "distance": 30},
    ],
}


def mock_create_graph(_):
    """
    Mock implementation of create_graph.
    Returns a simple adjacency dictionary to simulate a graph.
    """
    return {1: [(10, 2), (30, 3)], 2: [(10, 1), (15, 3)], 3: [(15, 2), (30, 1)], 4: []}


def mock_dijkstra(_, start_id, end_id):
    """
    Mock implementation of the Dijkstra algorithm.
    Returns pre-defined paths and distances for specific test cases.
    """
    if start_id == 1 and end_id == 3:
        return [1, 2, 3], 25, [1, 3], 30
    if start_id == 1 and end_id == 2:
        return [1, 2], 10, [], float("inf")
    if start_id == 1 and end_id == 1:
        return [1], 0, [], float("inf")
    return [], float("inf"), [], float("inf")


def test_get_route_valid_route(mocker):
    """
    Test if method get_route correctly calculates the route and distance when a valid route exists.
    """
    mocker.patch(
        "backend.src.navigation_service.navigation_service.create_graph",
        side_effect=mock_create_graph,
    )
    mocker.patch(
        "backend.src.navigation_service.navigation_service.dijkstra",
        side_effect=mock_dijkstra,
    )

    result = get_route("CityA", "CityC", data, headers={})
    assert result == {
        "route": {"0": "CityA", "1": "CityB", "2": "CityC"},
        "distance": 25,
        "alternative_route": {"0": "CityA", "1": "CityC"},
        "alternative_distance": 30,
    }


def test_get_route_no_connection(mocker):
    """
    Test if method get_route returns an error when the end city does
    not exist in the dataset.
    """
    mocker.patch(
        "backend.src.navigation_service.navigation_service.create_graph",
        side_effect=mock_create_graph,
    )
    mocker.patch(
        "backend.src.navigation_service.navigation_service.dijkstra",
        side_effect=mock_dijkstra,
    )

    result = get_route("CityA", "CityE", data, headers={})
    assert result == {"error": "City not found: CityA or CityE"}


def test_get_route_no_connection_between_cities(mocker):
    """
    Test if method get_route returns an error when there is no connection between
    the start and end cities.
    """
    mocker.patch(
        "backend.src.navigation_service.navigation_service.create_graph",
        side_effect=mock_create_graph,
    )
    mocker.patch(
        "backend.src.navigation_service.navigation_service.dijkstra",
        return_value=([], float("inf"), [], float("inf")),
    )

    result = get_route("CityA", "CityD", data, headers={})
    assert result == {"error": "No connection found between CityA and CityD"}
