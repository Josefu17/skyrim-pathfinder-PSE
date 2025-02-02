"""Dao file for the City entity"""

from sqlalchemy.orm import Session
from backend.src.database.schema.city import City

from backend.src.utils.helpers import get_logging_configuration

logger = get_logging_configuration()


class CityDao:
    """Data Access Object for City."""

    @staticmethod
    def get_cities_by_map_id(map_id: int, session: Session):
        """Get all cities of a map as a list."""
        return session.query(City).filter_by(map_id=map_id).all()

    @staticmethod
    def get_city_by_name(map_id: int, name: str, session: Session):
        """Get city by name."""
        return session.query(City).filter_by(map_id=map_id, name=name).first()

    @staticmethod
    def get_city_by_id(city_id: int, session: Session):
        """Get city by id."""
        return session.get(City, city_id)

    @staticmethod
    def save_city(city: City, session: Session) -> City:
        """Save a single city and return the saved city."""
        session.add(city)
        session.commit()
        return city

    @staticmethod
    def save_cities_bulk(cities: list[City], session: Session):
        """Save multiple cities in bulk."""
        try:
            session.bulk_save_objects(cities)
            session.commit()
            logger.info("Successfully inserted %s cities in bulk.", len(cities))
        except Exception as e:
            session.rollback()
            logger.error("Error during bulk insert of cities: %s", e)
            raise

    @staticmethod
    def delete_city(city_id: int, session: Session) -> bool:
        """Delete city if it exists and return True if deleted, else False."""
        city = session.get(City, city_id)
        if city:
            session.delete(city)
            session.commit()
            return True
        return False
