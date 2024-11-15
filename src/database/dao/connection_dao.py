"""Data Access Object for Connections."""

from sqlalchemy.orm import sessionmaker

from src.database.database import new_engine
from src.database.schema.connection import Connection

SESSION_MAKER = sessionmaker(bind=new_engine)
SESSION = SESSION_MAKER()


# Connections dao
class ConnectionDAO:
    """Data Access Object for Connections."""

    @staticmethod
    def get_all_connections():
        """get all connections."""
        return SESSION.query(Connection).all()

    @staticmethod
    def get_connection_by_parent_and_child(parent_city_id, child_city_id):
        """get connection by endpoints."""
        return (
            SESSION.query(Connection)
            .filter_by(parent_city_id=parent_city_id, child_city_id=child_city_id)
            .first()
        )

    @staticmethod
    def save_connection(connection):
        """save connection."""
        SESSION.add(connection)
        SESSION.commit()

    @staticmethod
    def save_connections_bulk(connections):
        """save multiple connections in bulk"""
        SESSION.add_all(connections)
        SESSION.commit()

    @staticmethod
    def delete_connection(connection_id):
        """delete connection."""
        connection = SESSION.query(Connection).get(connection_id)
        if connection:
            SESSION.delete(connection)
            SESSION.commit()
