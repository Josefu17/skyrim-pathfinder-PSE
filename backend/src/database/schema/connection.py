""" Python file for database class Connection"""

from sqlalchemy import ForeignKey, Column, Integer

from backend.src.database.schema.base import Base
from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


class Connection(Base):
    """Database class Connection"""

    __tablename__ = "connections"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    map_id: int = Column(
        Integer,
        ForeignKey("maps.id", name="connections_map_id_fkey", ondelete="CASCADE"),
        nullable=False,
    )
    parent_city_id: int = Column(
        Integer,
        ForeignKey("cities.id", name="connections_parent_city_id_fkey", ondelete="CASCADE"),
        nullable=False,
    )
    child_city_id: int = Column(
        Integer,
        ForeignKey("cities.id", name="connections_child_city_id_fkey", ondelete="CASCADE"),
        nullable=False,
    )

    def to_dict(self):
        """convert the object into dictionary"""
        connection_dict = {
            "id": self.id,
            "map_id": self.map_id,
            "parent_city_id": self.parent_city_id,
            "child_city_id": self.child_city_id,
        }
        logger.debug("Converting Connection to dictionary: %s", connection_dict)

    def __repr__(self):
        """Returns a string representation of a Connection object."""
        repr_str = (
            f"<Connection(id={self.id}, map_id={self.map_id}, "
            f"parent_city_id={self.parent_city_id}, child_city_id={self.child_city_id})>"
        )
        logger.debug("Connection representation: %s", repr_str)
        return repr_str

    def __eq__(self, other):
        if not isinstance(other, Connection):
            return False
        return (
            self.id == other.id
            and self.map_id == other.map_id
            and self.parent_city_id == other.parent_city_id
            and self.child_city_id == other.child_city_id
        )
