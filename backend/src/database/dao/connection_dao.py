"""Dao file for the Connection entity"""

from sqlalchemy.orm import Session
from backend.src.database.schema.connection import Connection

from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


class ConnectionDao:
    """Data Access Object for Connection."""

    @staticmethod
    def get_connection_by_parent_and_child(
        map_id: int, parent_city_id: int, child_city_id: int, session: Session
    ):
        """Get connection by parent and child city IDs."""
        return (
            session.query(Connection)
            .filter_by(map_id=map_id, parent_city_id=parent_city_id, child_city_id=child_city_id)
            .first()
        )

    @staticmethod
    def save_connections_bulk(connections: list[Connection], session: Session):
        """Save multiple connections in bulk."""
        try:
            session.bulk_save_objects(connections)
            session.commit()
            logger.info("Successfully inserted %s connections in bulk.", len(connections))
        except Exception as e:
            session.rollback()
            logger.error("Error during bulk insert of connections: %s", e)
            raise

    @staticmethod
    def get_connections_by_map_id(map_id: int, session: Session):
        """get all connections of a map."""
        return session.query(Connection).filter_by(map_id=map_id).all()
