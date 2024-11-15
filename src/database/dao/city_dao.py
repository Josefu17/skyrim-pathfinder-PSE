"""Data Access Object for City."""

from sqlalchemy.orm import sessionmaker

from src.database.database import new_engine
from src.database.schema.city import City

SESSION_MAKER = sessionmaker(bind=new_engine)
SESSION = SESSION_MAKER()


# Cities dao
class CityDAO:
    """Data Access Object for City."""

    @staticmethod
    def get_all_cities():
        """get all cities as list"""
        return SESSION.query(City).all()

    @staticmethod
    def get_city_by_name(name):
        """get city by name"""
        return SESSION.query(City).filter_by(name=name).first()

    @staticmethod
    def get_city_by_id(city_id):
        """get city by id"""
        return SESSION.query(City).get(city_id)

    @staticmethod
    def save_city(city):
        """save city"""
        SESSION.add(city)
        SESSION.commit()

    @staticmethod
    def delete_city(city_id):
        """delete city"""
        city = SESSION.query(City).get(city_id)
        if city:
            SESSION.delete(city)
            SESSION.commit()
