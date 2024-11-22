"""file to register all the database classes"""

# pylint: disable=unused-import
from backend.src.database.schema.city import City  # noqa
from backend.src.database.schema.connection import Connection  # noqa


# Register models by importing them
def register_models():
    """Ensure all models are registered with Base metadata."""
