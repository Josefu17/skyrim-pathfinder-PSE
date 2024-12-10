"""Data Access Object for Map"""

from sqlalchemy.orm import Session

from backend.src.database.schema.map import Map


class MapDao:
    """Data Access Object for database class Map"""

    @staticmethod
    def get_map(session: Session):
        """current logic: get the first map entry in db"""
        return session.query(Map).first()

    @staticmethod
    def save_map(map_obj: Map, session: Session):
        """save map and return saved map"""
        session.add(map_obj)
        session.commit()
        return map_obj
