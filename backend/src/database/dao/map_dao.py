"""Data Access Object for Map"""

from sqlalchemy.orm import Session

from backend.src.database.schema.map import Map


class MapDao:
    """Data Access Object for database class Map"""

    @staticmethod
    def get_map_by_name(session: Session, map_name: str) -> Map or None:
        """current logic: get the first map entry in db"""
        return session.query(Map).filter(Map.name == map_name).first()

    @staticmethod
    def get_map_by_id(map_id, session: Session) -> Map or None:
        """current logic: get the first map entry in db"""
        return session.query(Map).filter(Map.id == map_id).first()

    @staticmethod
    def save_map(map_obj: Map, session: Session) -> Map:
        """save a map and return saved map"""
        session.add(map_obj)
        session.commit()
        session.refresh(map_obj)
        return map_obj

    @staticmethod
    def get_map_id_by_name(session: Session, map_name: str) -> int:
        """get map_id by map name"""
        map_obj = MapDao.get_map_by_name(session, map_name)
        return map_obj.id

    @staticmethod
    def get_all_maps(session: Session) -> list[Map]:
        """get all maps"""
        return session.query(Map).all()
