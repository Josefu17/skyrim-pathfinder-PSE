"""Integration tests for User and UserDao"""

from backend.src.database.dao.user_dao import UserDao
from backend.src.database.schema.user import User


def test_save_and_get_user(db):
    """Test save and get user"""
    # Arrange
    user = User(username="Dragonborn")

    # Act
    UserDao.save_user(user, db)
    retrieved_user = UserDao.get_user_by_username("Dragonborn", db)

    # Assert
    assert retrieved_user is not None
    assert retrieved_user.username == "Dragonborn"


def test_get_all_users(db):
    """Test get all users"""
    # Arrange
    user1 = User(username="Dovahkiin")
    user2 = User(username="Alduin")

    # Act
    UserDao.save_user(user1, db)
    UserDao.save_user(user2, db)
    users = UserDao.get_all_users(db)

    # Assert
    assert len(users) == 2
    assert any(user.username == "Dovahkiin" for user in users)
    assert any(user.username == "Alduin" for user in users)


def test_get_user_by_id(db):
    """Test get user by ID"""
    # Arrange
    user = User(username="Paarthurnax")
    UserDao.save_user(user, db)

    # Act
    retrieved_user = UserDao.get_user_by_id(user.id, db)

    # Assert
    assert retrieved_user is not None
    assert retrieved_user.username == "Paarthurnax"


def test_user_exists_by_username(db):
    """Test user_exists_by_username"""
    # Arrange
    user = User(username="Delphine")
    UserDao.save_user(user, db)

    # Act
    exists = UserDao.user_exists_by_username("Delphine", db)
    not_exists = UserDao.user_exists_by_username("Ulfric", db)

    # Assert
    assert exists is True
    assert not_exists is False


def test_delete_user(db):
    """Test delete user"""
    # Arrange
    user = User(username="Esbern")
    UserDao.save_user(user, db)
    user_id = user.id

    # Act
    UserDao.delete_user(user_id, db)
    deleted_user = UserDao.get_user_by_id(user_id, db)

    # Assert
    assert deleted_user is None


def test_delete_user_by_username(db):
    """Test delete user by username"""
    # Arrange
    user = User(username="Astrid")
    UserDao.save_user(user, db)

    # Act
    UserDao.delete_user_by_username("Astrid", db)
    deleted_user = UserDao.get_user_by_username("Astrid", db)

    # Assert
    assert deleted_user is None


def test_user_exists(db):
    """Test user_exists method"""
    # Arrange
    user = User(username="Kodlak")
    UserDao.save_user(user, db)

    # Act
    exists = UserDao.user_exists(user.id, db)
    not_exists = UserDao.user_exists(9999, db)  # ID that doesn't exist

    # Assert
    assert exists is True
    assert not_exists is False
