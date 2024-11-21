"""Data Access Object for City."""

from src.database.schema.city import City


# Cities dao
class CityDAO:
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
    def save_city(city, session):
        """save city"""
        session.add(city)
        session.commit()

    @staticmethod
    def delete_city(city_id, session):
        """delete city"""
        city = session.get(City, city_id)
        if city:
            session.delete(city)
            session.commit()
