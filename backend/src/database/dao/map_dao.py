"""Data Access Object for Map"""

from backend.src.database.schema.map import Map


class MapDao:
    """Data Access Object for database class Map"""

    @staticmethod
    def get_map(session):
        """current logic: get the first map entry in db"""
        return session.query(Map).first()

    @staticmethod
    def save_map(map_obj, session):
        """save map"""
        session.add(map_obj)
        session.commit()
