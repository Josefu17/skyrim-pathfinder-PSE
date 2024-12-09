"""file to register all the database classes"""

# pylint: disable=unused-import
from backend.src.database.schema.city import City  # noqa
from backend.src.database.schema.connection import Connection  # noqa
from backend.src.database.schema.map import Map  # noqa
from backend.src.database.schema.user import User  # noqa


# Register models by importing them
def register_models():
    """Ensure all models are registered with Base metadata."""
