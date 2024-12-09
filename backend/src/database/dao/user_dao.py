"""File for User Data Access Object"""

from backend.src.database.schema.user import User


class UserDao:
    """Data Access Object for User"""

    @staticmethod
    def get_all_users(session):
        """get all users as list"""
        return session.query(User).all()

    @staticmethod
    def get_user_by_id(user_id, session):
        """get user by id"""
        return session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_username(username, session):
        """get user by username"""
        return session.query(User).filter(User.username == username).first()

    @staticmethod
    def save_user(user, session):
        """save a new User"""
        session.add(user)
        session.commit()

    @staticmethod
    def delete_user(user_id, session):
        """delete a user by id"""
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            session.commit()

    @staticmethod
    def delete_user_by_username(username, session):
        """delete a user by username"""
        user = session.query(User).filter(User.username == username).first()
        if user:
            session.delete(user)
            session.commit()

    @staticmethod
    def user_exists(user_id, session) -> bool:
        """convenience method to check if a user exists"""
        return session.query(User).filter(User.id == user_id).first() is not None

    @staticmethod
    def user_exists_by_username(username, session):
        """convenience method to check if a user with the username exists"""
        return session.query(User).filter(User.username == username).first() is not None
