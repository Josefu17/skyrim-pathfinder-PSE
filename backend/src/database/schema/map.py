"""Python file for database class Map"""

from sqlalchemy import Column, Integer, String

from backend.src.database.schema.base import Base
from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


class Map(Base):
    """Database class Map"""

    __tablename__ = "maps"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(255), unique=True, nullable=False)
    size_x: int = Column(Integer)
    size_y: int = Column(Integer)

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
