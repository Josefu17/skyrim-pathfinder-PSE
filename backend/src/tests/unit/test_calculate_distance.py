"""
Tests calculate_distance
"""

import math
from backend.src.navigation_service.navigation_service import calculate_distance


class City:
    """Dummy class"""

    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y

    def __str__(self):
        """String representation of the City instance."""
        return f"City({self.position_x}, {self.position_y})"

    def distance_to(self, other_city):
        """Calculate the distance to another city."""
        return math.sqrt(
            (other_city.position_x - self.position_x) ** 2
            + (other_city.position_y - self.position_y) ** 2
        )

    def to_dict(self):
        """convert object into dictionary"""
        return {
            "position_x": self.position_x,
            "position_y": self.position_y,
        }


def test_calculate_distance_same_point():
    """Test with identical points"""
    city_a = City(0, 0).to_dict()
    city_b = City(0, 0).to_dict()
    assert calculate_distance(city_a, city_b) == 0


def test_calculate_distance_horizontal():
    """Tests the distance between two points that are horizontally apart"""
    city_a = City(0, 0).to_dict()
    city_b = City(3, 0).to_dict()
    assert calculate_distance(city_a, city_b) == 3


def test_calculate_distance_vertical():
    """Tests the distance between two points that are vertically apart"""
    city_a = City(0, 0).to_dict()
    city_b = City(0, 4).to_dict()
    assert calculate_distance(city_a, city_b) == 4


def test_calculate_distance_diagonal():
    """Tests the distance between two points that are diagonally apart"""
    city_a = City(0, 0).to_dict()
    city_b = City(3, 4).to_dict()
    expected_distance = 5

    assert calculate_distance(city_a, city_b) == expected_distance


def test_calculate_distance_arbitrary_points():
    """Tests the distance between two random points"""
    city_a = City(1, 1).to_dict()
    city_b = City(4, 5).to_dict()
    expected_distance = math.sqrt((4 - 1) ** 2 + (5 - 1) ** 2)
    assert calculate_distance(city_a, city_b) == expected_distance
