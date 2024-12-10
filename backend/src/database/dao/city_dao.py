"""Data Access Object for City."""

from sqlalchemy.orm import Session

from backend.src.database.schema.city import City


class CityDao:
    """Data Access Object for City."""

    @staticmethod
    def get_all_cities(session):
        """get all cities as list"""
        return session.query(City).all()

    @staticmethod
    def get_city_by_name(name, session):
        """get city by name"""
        return session.query(City).filter_by(name=name).first()

    @staticmethod
    def get_city_by_id(city_id, session):
        """get city by id"""
        return session.get(City, city_id)

    @staticmethod
    def save_city(city: City, session: Session) -> City:
        """save city and return saved city"""
        session.add(city)
        session.commit()
        return city

    @staticmethod
    def delete_city(city_id, session) -> bool:
        """delete city if exists and return True if deleted, else False"""
        city = session.get(City, city_id)
        if city:
            session.delete(city)
            session.commit()
            return True
        return False
