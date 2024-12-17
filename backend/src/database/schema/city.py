""" Python file for database class City"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.database.schema.base import Base
from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


class City(Base):
    """Database class City"""

    __tablename__ = "city"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    position_x: Mapped[int] = mapped_column()
    position_y: Mapped[int] = mapped_column()

    def to_dict(self):
        """convert the object into dictionary"""
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
            f"<City(id={self.id}, name={self.name}, x={self.position_x}, y={self.position_y})>"
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
