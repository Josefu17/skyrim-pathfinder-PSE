"""integration tests for Connection and ConnectionDao"""

from backend.src.database.dao.connection_dao import ConnectionDao
from backend.src.database.schema.city import City
from backend.src.database.schema.connection import Connection


# Example test that includes setting up valid cities
def test_save_and_get_connection(db):
    """test save and get connection"""
    # Arrange
    city1 = City(name="Markarth", position_x=100, position_y=200)
    city2 = City(name="Riften", position_x=300, position_y=400)
    db.add(city1)
    db.add(city2)
    db.flush()

    # Act
    connection = Connection(parent_city_id=city1.id, child_city_id=city2.id)
    ConnectionDao.save_connection(connection, db)
    retrieved_connection = ConnectionDao.get_connection_by_parent_and_child(
        city1.id, city2.id, db
    )

    # Assert
    assert retrieved_connection is not None
    assert retrieved_connection.parent_city_id == city1.id
    assert retrieved_connection.child_city_id == city2.id


def test_get_all_connections(db):
    """test get all connections"""
    # Arrange
    city1 = City(name="Whiterun", position_x=100, position_y=300)
    city2 = City(name="Solitude", position_x=400, position_y=500)
    db.add(city1)
    db.add(city2)
    db.flush()

    connection1 = Connection(parent_city_id=city1.id, child_city_id=city2.id)
    connection2 = Connection(parent_city_id=city2.id, child_city_id=city1.id)
    ConnectionDao.save_connection(connection1, db)
    ConnectionDao.save_connection(connection2, db)

    # Act
    connections = ConnectionDao.get_all_connections(db)

    # Assert
    assert len(connections) == 2
    assert any(
        conn.parent_city_id == city1.id and conn.child_city_id == city2.id
        for conn in connections
    )
    assert any(
        conn.parent_city_id == city2.id and conn.child_city_id == city1.id
        for conn in connections
    )


def test_save_connections_bulk(db):
    """test save and get connections"""
    # Arrange
    city1 = City(name="Falkreath", position_x=100, position_y=200)
    city2 = City(name="Windhelm", position_x=500, position_y=600)
    db.add(city1)
    db.add(city2)
    db.flush()

    connection1 = Connection(parent_city_id=city1.id, child_city_id=city2.id)
    connection2 = Connection(parent_city_id=city2.id, child_city_id=city1.id)
    connections = [connection1, connection2]

    # Act
    ConnectionDao.save_connections_bulk(connections, db)
    retrieved_connections = ConnectionDao.get_all_connections(db)

    # Assert
    assert len(retrieved_connections) == 2
    assert any(
        conn.parent_city_id == city1.id and conn.child_city_id == city2.id
        for conn in retrieved_connections
    )
    assert any(
        conn.parent_city_id == city2.id and conn.child_city_id == city1.id
        for conn in retrieved_connections
    )


def test_delete_connection(db):
    """test delete connection"""
    # Arrange
    city1 = City(name="Riverwood", position_x=200, position_y=300)
    city2 = City(name="Helgen", position_x=400, position_y=500)
    db.add(city1)
    db.add(city2)
    db.flush()

    connection = Connection(parent_city_id=city1.id, child_city_id=city2.id)
    ConnectionDao.save_connection(connection, db)
    connection_id = connection.id

    # Act
    ConnectionDao.delete_connection(connection_id, db)
    deleted_connection = db.get(Connection, connection_id)

    # Assert
    assert deleted_connection is None
