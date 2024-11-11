""" Creates Tables for database """

from sqlalchemy import Column, Integer, ForeignKey
from src.database.schema.city import Base


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
            "parent_city_id": self.parent_city_id,
            "child_city_id": self.child_city_id,
        }

    def __repr__(self):
        """Returns a string representation of a Connection object."""
        return (
            f"<Connection(id={self.id}, parent_city_id={self.parent_city_id}, "
            f"child_city_id={self.child_city_id})>"
        )
