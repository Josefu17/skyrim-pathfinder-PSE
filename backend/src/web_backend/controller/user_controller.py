"""User controller module for the Flask app."""

from flask import request, jsonify
from opentelemetry.trace import get_tracer

from backend.src.database.dao.user_dao import UserDao
from backend.src.database.db_connection import get_db_session
from backend.src.database.schema.user import User
from backend.src.utils.helpers import get_logging_configuration, metrics_logger
from backend.src.utils.tracing import set_span_error_flags

logger = get_logging_configuration()
tracer = get_tracer("user-controller")

REGISTER = "/auth/register"
LOGIN = "/auth/login"

USER_NAME_REQUIRED = "Username is required"


def init_user_routes(app):
    """Initialize all routes for the Flask app."""
    app.route(REGISTER, methods=["POST"])(register_user)
    app.route(LOGIN, methods=["POST"])(login_user)


def register_user():
    """Register a new user."""
    with tracer.start_as_current_span("register_user") as span:
        data = request.get_json()
        username = data.get("username")
        span.set_attribute("username", username)

        if not username:
            return handle_user_name_required(span)

        with get_db_session() as session:
            if UserDao.user_exists_by_username(username, session):
                metrics_logger.incr("m_error_existing_username")
                set_span_error_flags(span, ValueError("Username already exists"))
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
    with tracer.start_as_current_span("login_user") as span:
        data = request.get_json()
        username = data.get("username")
        span.set_attribute("username", username)

        if not username:
            return handle_user_name_required(span)

        with get_db_session() as session:
            user = UserDao.get_user_by_username(username, session)

            if not user:
                metrics_logger.incr("m_error_user_not_found")
                set_span_error_flags(span, ValueError("User not found"))
                return jsonify({"error": "User not found"}), 404

        logger.info("Logging in user: %s", username)
        metrics_logger.incr("m_logged_in_users")
        return (
            jsonify(
                {
                    "message": f"User {username} logged in successfully.",
                    "user": {"username": username, "id": user.id},
                }
            ),
            200,
        )


def handle_user_name_required(span):
    """missing username handler"""
    metrics_logger.incr("m_error_missing_username")
    set_span_error_flags(span, ValueError(USER_NAME_REQUIRED))
    return jsonify({"error": USER_NAME_REQUIRED}), 400
