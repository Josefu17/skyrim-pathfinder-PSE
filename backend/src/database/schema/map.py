"""Python file for database class Map"""

from sqlalchemy import Column, Integer, String

from backend.src.database.schema.base import Base
from backend.src.logging_config import get_logging_configuration

logger = get_logging_configuration()


class Map(Base):
    """Database class Map"""

    __tablename__ = "maps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    size_x = Column(Integer, nullable=False)
    size_y = Column(Integer, nullable=False)

    def to_dict(self):
        """regular to_dict method for map"""
        return {
            "id": self.id,
            "name": self.name,
            "size_x": self.size_x,
            "size_y": self.size_y,
        }

    def __eq__(self, other):
        if not isinstance(other, Map):
            return False
        return (
            self.id == other.id
            and self.name == other.name
            and self.size_x == other.size_x
            and self.size_y == other.size_y
        )

    def __repr__(self):
        """Returns a string representation of a Connection object."""
        repr_str = (
            f"<Map(id={self.id}, name={self.name}, size_x={self.size_x}, size_y={self.size_y})>"
        )
        logger.debug("Map representation: %s", repr_str)
        return repr_str
