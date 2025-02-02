"""integration tests for City and CityDao"""

from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError

from backend.src.database.dao.city_dao import CityDao
from backend.src.database.schema.city import City
from backend.src.tests.integration.dao_tests.test_connection_dao_it import fabricate_and_commit_map


def test_save_and_get_city(db):
    """test save and get city"""
    # Arrange
    test_map = fabricate_and_commit_map(db)
    city = City(map_id=test_map.id, name="Markarth", position_x=100, position_y=200)

    # Act
    CityDao.save_city(city, db)
    retrieved_city = CityDao.get_city_by_name(test_map.id, "Markarth", db)

    # Assert
    assert retrieved_city is not None
    assert retrieved_city.name == "Markarth"
    assert retrieved_city.position_x == 100
    assert retrieved_city.position_y == 200


def test_get_all_cities(db):
    """test get all cities"""
    # Arrange
    test_map = fabricate_and_commit_map(db)

    city1 = City(map_id=test_map.id, name="Whiterun", position_x=150, position_y=300)
    city2 = City(map_id=test_map.id, name="Riften", position_x=300, position_y=500)

    # Act
    CityDao.save_city(city1, db)
    CityDao.save_city(city2, db)
    cities = CityDao.get_cities_by_map_id(1, db)

    # Assert
    assert len(cities) == 2
    assert any(city.name == "Whiterun" for city in cities)
    assert any(city.name == "Riften" for city in cities)


def test_get_city_by_id(db):
    """test get city by id"""
    # Arrange
    test_map = fabricate_and_commit_map(db)

    city = City(map_id=test_map.id, name="Solitude", position_x=500, position_y=600)
    CityDao.save_city(city, db)

    # Act
    retrieved_city = CityDao.get_city_by_id(city.id, db)

    # Assert
    assert retrieved_city is not None
    assert retrieved_city.name == "Solitude"
    assert retrieved_city.position_x == 500
    assert retrieved_city.position_y == 600


def test_delete_city(db):
    """test delete city"""
    # Arrange
    test_map = fabricate_and_commit_map(db)

    city = City(map_id=test_map.id, name="Windhelm", position_x=700, position_y=800)
    CityDao.save_city(city, db)
    city_id = city.id

    # Act
    CityDao.delete_city(city_id, db)
    deleted_city = CityDao.get_city_by_id(city_id, db)

    # Assert
    assert deleted_city is None


def test_save_cities_bulk(db):
    """test save cities in bulk"""
    # Arrange
    test_map = fabricate_and_commit_map(db)

    city1 = City(map_id=test_map.id, name="Dawnstar", position_x=100, position_y=200)
    city2 = City(map_id=test_map.id, name="Falkreath", position_x=300, position_y=400)
    cities = [city1, city2]

    # Act
    CityDao.save_cities_bulk(cities, db)
    retrieved_cities = CityDao.get_cities_by_map_id(test_map.id, db)

    # Assert
    assert len(retrieved_cities) == 2
    assert any(city.name == "Dawnstar" for city in retrieved_cities)
    assert any(city.name == "Falkreath" for city in retrieved_cities)


def test_save_cities_bulk_exception(db):
    """test save cities in bulk with exception"""
    # Arrange
    test_map = fabricate_and_commit_map(db)
    city1 = City(map_id=test_map.id, name="Dawnstar", position_x=100, position_y=200)
    city2 = City(map_id=test_map.id, name="Falkreath", position_x=300, position_y=400)
    cities = [city1, city2]

    # Mock the rollback method
    db.rollback = MagicMock()

    # Act & Assert
    with patch.object(db, "bulk_save_objects", side_effect=SQLAlchemyError("Database error")):
        try:
            CityDao.save_cities_bulk(cities, db)
        except SQLAlchemyError as e:
            assert str(e) == "Database error"
            db.rollback.assert_called_once()
