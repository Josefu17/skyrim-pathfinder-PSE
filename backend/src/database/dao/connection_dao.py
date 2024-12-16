"""Data Access Object for Connections."""

from sqlalchemy.orm import Session

from backend.src.database.schema.connection import Connection


class ConnectionDao:
    """Data Access Object for Connections."""

    @staticmethod
    def get_all_connections(session: Session):
        """get all connections."""
        return session.query(Connection).all()

    @staticmethod
    def get_connection_by_parent_and_child(parent_city_id, child_city_id, session: Session):
        """get connection by endpoints."""
        return (
            session.query(Connection)
            .filter_by(parent_city_id=parent_city_id, child_city_id=child_city_id)
            .first()
        )

    @staticmethod
    def save_connection(connection: Connection, session: Session) -> Connection:
        """save connection, return the saved connection"""
        session.add(connection)
        session.commit()
        return connection

    @staticmethod
    def save_connections_bulk(connections, session: Session) -> list:
        """save multiple connections in bulk"""
        session.add_all(connections)
        session.commit()
        return connections

    @staticmethod
    def delete_connection(connection_id, session) -> bool:
        """delete connection, return True if deleted, else False"""
        connection = session.get(Connection, connection_id)
        if connection:
            session.delete(connection)
            session.commit()
            return True
        return False
