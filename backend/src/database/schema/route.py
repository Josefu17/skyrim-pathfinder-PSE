"""Python file for database class Route"""

import dataclasses
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Dict

from sqlalchemy import ForeignKey, String, Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSON

from backend.src.database.schema.base import Base
from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


class Route(Base):
    """Database class Route"""

    __tablename__ = "routes"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: int = Column(
        Integer,
        ForeignKey("users.id", name="routes_user_id_fkey", ondelete="CASCADE"),
        nullable=False,
    )
    map_id: int = Column(
        Integer,
        ForeignKey("maps.id", name="routes_map_id_fkey", ondelete="CASCADE"),
        nullable=False,
    )
    startpoint: str = Column(String(255))
    endpoint: str = Column(String(255))
    created_at: datetime = Column(DateTime, default=datetime.now(timezone.utc))
    route: Dict = Column(JSON)

    def to_dict(self):
        """Convert the object into dictionary"""
        route_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "map_id": self.map_id,
            "startpoint": self.startpoint,
            "endpoint": self.endpoint,
            "created_at": self.created_at,
            "route": self.route,
        }
        logger.debug("Converting Route to dictionary: %s", route_dict)
        return route_dict

    def __repr__(self):
        """Returns a string representation of a Route object"""
        repr_str = (
            f"<Route(id={self.id}, user_id={self.user_id}, map_id={self.map_id}, "
            f"startpoint={self.startpoint}, endpoint={self.endpoint}, created_at={self.created_at}"
            f", route={self.route})>"
        )
        logger.debug("Route representation: %s", repr_str)
        return repr_str


@dataclass
class OptionalRouteFilters:
    """Encapsulate optional filtering parameters for routes."""

    map_id: Optional[int] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    startpoint: Optional[str] = None
    endpoint: Optional[str] = None


@dataclass
class RouteFilter:
    """Data class to store filtering information for Routes to be used in RouteDao"""

    user_id: int
    field: str = "created_at"
    limit: int = 10
    descending: bool = True
    optional_filters: OptionalRouteFilters = dataclasses.field(default_factory=OptionalRouteFilters)

    def __post_init__(self):
        # Ensure optional_filters is a dictionary
        self.optional_filters = self.optional_filters or {}

    def destructure(self):
        """Return the individual fields for destructuring"""
        return (
            self.user_id,
            self.field,
            self.limit,
            self.descending,
            self.optional_filters.map_id,
            self.optional_filters.from_date,
            self.optional_filters.to_date,
            self.optional_filters.startpoint,
            self.optional_filters.endpoint,
        )
