"""User controller module for the Flask app."""

from flask import request, jsonify

from backend.src.utils.helpers import get_logging_configuration
from backend.src.database.schema.user import User
from backend.src.database.db_connection import get_db_session
from backend.src.database.dao.user_dao import UserDao

logger = get_logging_configuration()

REGISTER = "/auth/register"
LOGIN = "/auth/login"


def init_user_routes(app):
    """Initialize all routes for the Flask app."""
    app.route(REGISTER, methods=["POST"])(register_user)
    app.route(LOGIN, methods=["POST"])(login_user)


def register_user():
    """Register a new user."""
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    with get_db_session() as session:
        if UserDao.user_exists_by_username(username, session):
            return jsonify({"error": "Username already exists"}), 400

        user = User(username=username)
        UserDao.save_user(user, session)
        session.refresh(user)

    logger.info("Registering new user: %s", username)
    return (
        jsonify(
            {
                "message": f"User {username} registered successfully.",
                "user": {"username": username, "id": user.id},
            }
        ),
        201,
    )


def login_user():
    """Login an existing user."""
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    with get_db_session() as session:
        user = UserDao.get_user_by_username(username, session)

        if not user:
            return jsonify({"error": "User not found"}), 404

    logger.info("Logging in user: %s", username)
    return (
        jsonify(
            {
                "message": f"User {username} logged in successfully.",
                "user": {"username": username, "id": user.id},
            }
        ),
        200,
    )
