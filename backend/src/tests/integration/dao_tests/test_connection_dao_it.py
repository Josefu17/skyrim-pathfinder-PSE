"""integration tests for Connection and ConnectionDao"""

from unittest.mock import Mock
import pytest
from sqlalchemy.orm import Session
from backend.src.database.dao.connection_dao import ConnectionDao
from backend.src.database.schema.city import City
from backend.src.database.schema.connection import Connection
from backend.src.database.schema.map import Map


# Example test that includes setting up valid cities
def test_save_and_get_connection(db):
    """test save and get connection"""
    # Arrange
    test_map = fabricate_and_commit_map(db)

    city1 = City(map_id=test_map.id, name="Markarth", position_x=100, position_y=200)
    city2 = City(map_id=test_map.id, name="Riften", position_x=300, position_y=400)
    db.add(city1)
    db.add(city2)
    db.flush()

    # Act
    connection = Connection(map_id=test_map.id, parent_city_id=city1.id, child_city_id=city2.id)
    ConnectionDao.save_connections_bulk([connection], db)
    retrieved_connection = ConnectionDao.get_connection_by_parent_and_child(
        1, city1.id, city2.id, db
    )

    # Assert
    assert retrieved_connection is not None
    assert retrieved_connection.parent_city_id == city1.id
    assert retrieved_connection.child_city_id == city2.id


def fabricate_connections(city1, city2, test_map):
    """fabricate and insert dummy connections"""
    connection1 = Connection(map_id=test_map.id, parent_city_id=city1.id, child_city_id=city2.id)
    connection2 = Connection(map_id=test_map.id, parent_city_id=city2.id, child_city_id=city1.id)
    return [connection1, connection2]


def fabricate_and_commit_map(db):
    """fabricate and commit test map"""
    test_map = Map(name="Test Map", size_x=100, size_y=100)
    db.add(test_map)
    db.flush()
    return test_map


def test_save_connections_bulk(db):
    """test save and get connections"""
    # Arrange
    test_map = fabricate_and_commit_map(db)

    city1 = City(map_id=test_map.id, name="Falkreath", position_x=100, position_y=200)
    city2 = City(map_id=test_map.id, name="Windhelm", position_x=500, position_y=600)

    db.add(city1)
    db.add(city2)
    db.flush()

    connections = fabricate_connections(city1, city2, test_map)

    # Act
    ConnectionDao.save_connections_bulk(connections, db)
    retrieved_connections = ConnectionDao.get_connections_by_map_id(1, db)

    # Assert
    assert_connections_exist(retrieved_connections, [(city1.id, city2.id), (city2.id, city1.id)])


def test_save_connections_bulk_exception_handling():
    """Test exception handling in save_connections_bulk method."""
    # Arrange
    session = Mock(spec=Session)
    connections = [Mock(spec=Connection)]
    session.bulk_save_objects.side_effect = Exception("Test exception")

    # Act & Assert
    with pytest.raises(Exception, match="Test exception"):
        ConnectionDao.save_connections_bulk(connections, session)

    session.rollback.assert_called_once()
    session.commit.assert_not_called()


def assert_connections_exist(connections, expected_pairs):
    """
    Assert that the given connections contain the expected parent-child pairs.
    :param connections: List of Connection objects.
    :param expected_pairs: List of (parent_city_id, child_city_id) tuples.
    """
    assert len(connections) == len(expected_pairs)

    for parent_id, child_id in expected_pairs:
        assert any(
            conn.parent_city_id == parent_id and conn.child_city_id == child_id
            for conn in connections
        )
