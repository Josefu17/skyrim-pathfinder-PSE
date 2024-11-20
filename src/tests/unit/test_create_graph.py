"""
Tests create_graph()
"""

from collections import defaultdict
from src.navigation_service.navigation_service import create_graph

# Mock data
data = {
    "cities": [
        {"id": 1, "name": "CityA", "x": 0, "y": 0},
        {"id": 2, "name": "CityB", "x": 0, "y": 10},
        {"id": 3, "name": "CityC", "x": 10, "y": 0},
    ],
    "connections": [
        {"parent_city_id": 1, "child_city_id": 2},
        {"parent_city_id": 2, "child_city_id": 3},
    ],
}

# Mock functions
def mock_get_city_by_id(cities, city_id):
    """
    Mock for get_city_by_id. Returns a city object if found; otherwise, None.
    """
    for city in cities:
        if city["id"] == city_id:
            return city
    return None

def mock_calculate_distance(city_1, city_2):
    """
    Mock for calculate_distance. Returns a fixed distance based on city IDs.
    """
    return abs(city_1["x"] - city_2["x"]) + abs(city_1["y"] - city_2["y"])

def test_create_graph_valid_data(mocker):
    """
    Test if create_graph constructs a valid graph from correct input data.
    """
    mocker.patch("src.navigation_service.navigation_service.get_city_by_id",
                 side_effect=mock_get_city_by_id)
    mocker.patch("src.navigation_service.navigation_service.calculate_distance",
                 side_effect=mock_calculate_distance)

    result = create_graph(data)

    # Expected graph structure
    expected_graph = defaultdict(list, {
        1: [(10, 2)],
        2: [(10, 1), (20, 3)],
        3: [(20, 2)],
    })
    assert result == expected_graph

def test_create_graph_missing_city(mocker):
    """
    Test if create_graph skips connections with missing cities.
    """
    mocker.patch("src.navigation_service.navigation_service.get_city_by_id",
                 side_effect=lambda cities, city_id:
                 None if city_id == 3 else mock_get_city_by_id(cities, city_id))
    mocker.patch("src.navigation_service.navigation_service.calculate_distance",
                 side_effect=mock_calculate_distance)

    result = create_graph(data)

    # Graph should exclude invalid connections
    expected_graph = defaultdict(list, {
        1: [(10, 2)],
        2: [(10, 1)],
    })
    assert result == expected_graph

def test_create_graph_empty_data():
    """
    Test if create_graph handles empty input data gracefully.
    """
    empty_data = {"cities": [], "connections": []}
    result = create_graph(empty_data)

    # Expected empty graph
    expected_graph = defaultdict(list)
    assert result == expected_graph

def test_create_graph_no_connections(mocker):
    """
    Test if create_graph handles data with no connections.
    """
    data_no_connections = {
        "cities": [
            {"id": 1, "name": "CityA", "x": 0, "y": 0},
            {"id": 2, "name": "CityB", "x": 0, "y": 10},
        ],
        "connections": []
    }

    mocker.patch("src.navigation_service.navigation_service.get_city_by_id",
                 side_effect=mock_get_city_by_id)
    mocker.patch("src.navigation_service.navigation_service.calculate_distance",
                 side_effect=mock_calculate_distance)

    result = create_graph(data_no_connections)

    # Graph should have no edges
    expected_graph = defaultdict(list)
    assert result == expected_graph
