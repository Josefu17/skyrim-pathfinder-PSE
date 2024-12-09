""" Python file for database class Connection"""

from sqlalchemy import Column, Integer, ForeignKey

from backend.src.database.schema.base import Base
from backend.src.logging_config import get_logging_configuration

logger = get_logging_configuration()


class Connection(Base):
    """Database class Connection"""

    __tablename__ = "connections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    child_city_id = Column(Integer, ForeignKey("city.id"), nullable=False)

    def to_dict(self):
        """convert object into dictionary"""
        connection_dict = {
            "id": self.id,
            "parent_city_id": self.parent_city_id,
            "child_city_id": self.child_city_id,
        }
        logger.debug("Converting Connection to dictionary: %s", connection_dict)

    def __repr__(self):
        """Returns a string representation of a Connection object."""
        repr_str = (
            f"<Connection(id={self.id}, parent_city_id={self.parent_city_id}, "
            f"child_city_id={self.child_city_id})>"
        )
        logger.debug("Connection representation: %s", repr_str)
        return repr_str

    def __eq__(self, other):
        if not isinstance(other, Connection):
            return False
        return (
            self.id == other.id
            and self.parent_city_id == other.parent_city_id
            and self.child_city_id == other.child_city_id
        )
