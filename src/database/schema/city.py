""" Python file for database class City"""

from sqlalchemy import Column, Integer, String
from src.database.schema.base import Base


class City(Base):
    """Database class City"""

    __tablename__ = "city"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)

    def to_dict(self):
        """convert object into dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "position_x": self.position_x,
            "position_y": self.position_y,
        }

    def __repr__(self):
        """Returns a string representation of a City object."""
        return (
            f"<City(id={self.id}, name={self.name}, x={self.position_x}, "
            f"y={self.position_y})>"
        )
