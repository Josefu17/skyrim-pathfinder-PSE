"""Integration tests for Map and MapDao"""

from backend.src.database.dao.map_dao import MapDao
from backend.src.database.schema.map import Map


def test_save_and_get_map(db):
    """Test save and get map"""
    # Arrange
    map_obj = Map(name="Tamriel", size_x=1000, size_y=2000)

    # Act
    MapDao.save_map(map_obj, db)
    retrieved_map = MapDao.get_map_by_name(db, "Tamriel")

    # Assert
    assert retrieved_map is not None
    assert retrieved_map.name == "Tamriel"
    assert retrieved_map.size_x == 1000
    assert retrieved_map.size_y == 2000


def test_save_multiple_maps_and_get_first(db):
    """Test saving multiple maps and ensuring only the first is retrieved"""
    # Arrange
    map1 = Map(name="Tamriel", size_x=1000, size_y=2000)
    map2 = Map(name="Skyrim", size_x=500, size_y=800)

    # Act
    MapDao.save_map(map1, db)
    MapDao.save_map(map2, db)
    retrieved_map = MapDao.get_map_by_name(db, "Tamriel")

    # Assert
    assert retrieved_map is not None
    assert retrieved_map.name == "Tamriel"
    assert retrieved_map.size_x == 1000
    assert retrieved_map.size_y == 2000


def test_get_map_id_by_name(db):
    """Test get_map_id_by_name method"""
    # Arrange
    map_name = "Tamriel"
    map_obj = Map(name=map_name, size_x=1000, size_y=2000)
    MapDao.save_map(map_obj, db)

    # Act
    map_id = MapDao.get_map_id_by_name(db, map_name)

    # Assert
    assert map_id == map_obj.id
