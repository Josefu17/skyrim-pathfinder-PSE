""" Python file for database class City"""

from sqlalchemy import Column, Integer, String

from backend.src.database.schema.base import Base
from backend.src.logging_config import get_logging_configuration

logger = get_logging_configuration()


class City(Base):
    """Database class City"""

    __tablename__ = "city"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)

    def to_dict(self):
        """convert object into dictionary"""
        city_dict = {
            "id": self.id,
            "name": self.name,
            "position_x": self.position_x,
            "position_y": self.position_y,
        }
        logger.debug("Converting City to dictionary: %s", city_dict)
        return city_dict

    def __repr__(self):
        """Returns a string representation of a City object."""
        repr_str = (
            f"<City(id={self.id}, name={self.name}, x={self.position_x}, "
            f"y={self.position_y})>"
        )
        logger.debug("City representation: %s", repr_str)
        return repr_str

    def __eq__(self, other):
        if not isinstance(other, City):
            return False
        return (
            self.name == other.name
            and self.position_x == other.position_x
            and self.position_y == other.position_y
            and self.id == other.id
        )
