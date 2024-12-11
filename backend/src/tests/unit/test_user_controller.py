"""
Tests for the user controller.
"""

from unittest.mock import patch, MagicMock


@patch("backend.src.web_backend.controller.user_controller.UserDao")
@patch("backend.src.web_backend.controller.user_controller.get_db_session")
def test_register_user_success(mock_get_db_session, mock_user_dao, client):
    """
    Test registering a new user successfully.
    """
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_user_dao.user_exists_by_username.return_value = False

    def mock_save_user(user, session):  # pylint: disable=unused-argument
        user.id = 1
        return user

    mock_user_dao.save_user.side_effect = mock_save_user

    response = client.post("/auth/register", json={"username": "testuser"})
    assert response.status_code == 201
    assert response.json == {
        "message": "User testuser registered successfully.",
        "user": {"username": "testuser", "id": 1},
    }
    mock_user_dao.save_user.assert_called_once()


@patch("backend.src.web_backend.controller.user_controller.UserDao")
def test_register_user_missing_username(
    mock_user_dao,
    client,
):
    """
    Test registering a new user without a username.
    """
    response = client.post("/auth/register", json={})
    assert response.status_code == 400
    assert response.json == {"error": "Username is required"}
    mock_user_dao.save_user.assert_not_called()


@patch("backend.src.web_backend.controller.user_controller.UserDao")
@patch("backend.src.web_backend.controller.user_controller.get_db_session")
def test_user_login_success(mock_get_db_session, mock_user_dao, client):
    """
    Test logging in an existing user successfully.
    """
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session

    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user_dao.get_user_by_username.return_value = mock_user

    response = client.post("/auth/login", json={"username": "testuser"})
    assert response.status_code == 200
    assert response.json == {
        "message": "User testuser logged in successfully.",
        "user": {"username": "testuser", "id": 1},
    }
    mock_user_dao.get_user_by_username.assert_called_once()


@patch("backend.src.web_backend.controller.user_controller.UserDao")
def test_user_login_missing_username(
    mock_user_dao,
    client,
):
    """
    Test logging in without providing a username.
    """
    response = client.post("/auth/login", json={})
    assert response.status_code == 400
    assert response.json == {"error": "Username is required"}
    mock_user_dao.get_user_by_username.assert_not_called()


@patch("backend.src.web_backend.controller.user_controller.UserDao")
@patch("backend.src.web_backend.controller.user_controller.get_db_session")
def test_user_login_user_not_found(mock_get_db_session, mock_user_dao, client):
    """
    Test logging in with a non-existent user.
    """
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_user_dao.get_user_by_username.return_value = None

    response = client.post("/auth/login", json={"username": "nonexistentuser"})
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}
    mock_user_dao.get_user_by_username.assert_called_once()
