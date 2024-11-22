"""integration tests for City and CityDao"""

from backend.src.database.dao.city_dao import CityDAO
from backend.src.database.schema.city import City


def test_save_and_get_city(db):
    """test save and get city"""
    # Arrange
    city = City(name="Markarth", position_x=100, position_y=200)

    # Act
    CityDAO.save_city(city, db)
    retrieved_city = CityDAO.get_city_by_name("Markarth", db)

    # Assert
    assert retrieved_city is not None
    assert retrieved_city.name == "Markarth"
    assert retrieved_city.position_x == 100
    assert retrieved_city.position_y == 200


def test_get_all_cities(db):
    """test get all cities"""
    # Arrange
    city1 = City(name="Whiterun", position_x=150, position_y=300)
    city2 = City(name="Riften", position_x=300, position_y=500)

    # Act
    CityDAO.save_city(city1, db)
    CityDAO.save_city(city2, db)
    cities = CityDAO.get_all_cities(db)

    # Assert
    assert len(cities) == 2
    assert any(city.name == "Whiterun" for city in cities)
    assert any(city.name == "Riften" for city in cities)


def test_get_city_by_id(db):
    """test get city by id"""
    # Arrange
    city = City(name="Solitude", position_x=500, position_y=600)
    CityDAO.save_city(city, db)

    # Act
    retrieved_city = CityDAO.get_city_by_id(city.id, db)

    # Assert
    assert retrieved_city is not None
    assert retrieved_city.name == "Solitude"
    assert retrieved_city.position_x == 500
    assert retrieved_city.position_y == 600


def test_delete_city(db):
    """test delete city"""
    # Arrange
    city = City(name="Windhelm", position_x=700, position_y=800)
    CityDAO.save_city(city, db)
    city_id = city.id

    # Act
    CityDAO.delete_city(city_id, db)
    deleted_city = CityDAO.get_city_by_id(city_id, db)

    # Assert
    assert deleted_city is None
