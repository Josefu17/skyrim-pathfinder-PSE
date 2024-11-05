""" Creates Tables for database """

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cities(Base):
    """Creates cities table"""

    __tablename__ = "cities"
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


class Connections(Base):
    """Creates connections table"""

    __tablename__ = "connections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    child_city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    def to_dict(self):
        """convert object into dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "position_x": self.position_x,
            "position_y": self.position_y,
        }

    def __repr__(self):
        """Returns a string representation of a Connection object."""
        return (
            f"<Connection(id={self.id}, parent_city_id={self.parent_city_id}, "
            f"child_city_id={self.child_city_id})>"
        )
