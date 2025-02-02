""" Python file for database class City"""

from sqlalchemy import ForeignKey, String, Column, Integer

from backend.src.database.schema.base import Base
from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


class City(Base):
    """Database class City"""

    __tablename__ = "cities"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    map_id: int = Column(
        Integer,
        ForeignKey("maps.id", name="cities_map_id_fkey", ondelete="CASCADE"),
        nullable=False,
    )
    name: str = Column(String(255))
    position_x: int = Column(Integer)
    position_y: int = Column(Integer)

    def to_dict(self):
        """convert the object into dictionary"""
        city_dict = {
            "id": self.id,
            "map_id": self.map_id,
            "name": self.name,
            "position_x": self.position_x,
            "position_y": self.position_y,
        }
        logger.debug("Converting City to dictionary: %s", city_dict)
        return city_dict

    def __repr__(self):
        """Returns a string representation of a City object."""
        repr_str = (
            f"<City(id={self.id}, map_id{self.map_id}, name={self.name}, "
            f"x={self.position_x}, y={self.position_y})>"
        )
        logger.debug("City representation: %s", repr_str)
        return repr_str

    def __eq__(self, other):
        if not isinstance(other, City):
            return False
        return (
            self.id == other.id
            and self.map_id == other.map_id
            and self.name == other.name
            and self.position_x == other.position_x
            and self.position_y == other.position_y
        )
