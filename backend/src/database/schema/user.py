"""Python file for database class User"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.database.schema.base import Base
from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


class User(Base):
    """Database class User"""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)

    def to_dict(self):
        """convert User into dictionary"""
        user_dict = {"id": self.id, "username": self.username}
        logger.debug("Converting User to dictionary: %s", user_dict)
        return user_dict

    def __repr__(self):
        """Returns a string representation of User"""
        repr_str = f"<User(id={self.id}, username={self.username})>"
        logger.debug("User representation: %s", repr_str)
        return repr_str

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id and self.username == other.username
