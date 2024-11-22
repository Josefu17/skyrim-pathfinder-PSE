"""
Tests get_city_by_id()
"""

from backend.src.navigation_service.navigation_service import get_city_by_id


def test_get_city_by_id_valid_id():
    """
    Test if method get_city_by_id returns the correct city dictionary when a valid ID is provided.
    """
    cities = [
        {"id": 1, "name": "CityA"},
        {"id": 2, "name": "CityB"},
        {"id": 3, "name": "CityC"},
    ]
    result = get_city_by_id(cities, 2)
    assert result == {"id": 2, "name": "CityB"}


def test_get_city_by_id_invalid_id():
    """
    Test if method get_city_by_id returns None when an invalid ID is provided.
    """
    cities = [
        {"id": 1, "name": "CityA"},
        {"id": 2, "name": "CityB"},
    ]
    result = get_city_by_id(cities, 99)
    assert result is None


def test_get_city_by_id_empty_list():
    """
    Test if method get_city_by_id returns None when the cities list is empty.
    """
    cities = []
    result = get_city_by_id(cities, 1)
    assert result is None


def test_get_city_by_id_duplicate_ids():
    """
    Test if method get_city_by_id correctly returns the first city when duplicate IDs are present.
    """
    cities = [
        {"id": 1, "name": "CityA"},
        {"id": 1, "name": "CityDuplicate"},
    ]
    result = get_city_by_id(cities, 1)
    assert result == {"id": 1, "name": "CityA"}
