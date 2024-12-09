"""Data Access Object for Connections."""

from backend.src.database.schema.connection import Connection


# Connections dao
class ConnectionDao:
    """Data Access Object for Connections."""

    @staticmethod
    def get_all_connections(session):
        """get all connections."""
        return session.query(Connection).all()

    @staticmethod
    def get_connection_by_parent_and_child(parent_city_id, child_city_id, session):
        """get connection by endpoints."""
        return (
            session.query(Connection)
            .filter_by(parent_city_id=parent_city_id, child_city_id=child_city_id)
            .first()
        )

    @staticmethod
    def save_connection(connection, session):
        """save connection."""
        session.add(connection)
        session.commit()

    @staticmethod
    def save_connections_bulk(connections, session):
        """save multiple connections in bulk"""
        session.add_all(connections)
        session.commit()

    @staticmethod
    def delete_connection(connection_id, session):
        """delete connection."""
        connection = session.get(Connection, connection_id)
        if connection:
            session.delete(connection)
            session.commit()
