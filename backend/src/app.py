"""Main module to start the backend application."""

import os

from flask import Flask
from flask_cors import CORS

from backend.src.database.db_connection import get_db_session
from backend.src.map_service.map_service import fetch_and_store_map_data_if_needed
from backend.src.utils.helpers import get_logging_configuration
from backend.src.utils.tracing import setup_tracing
from backend.src.web_backend.controller import health_controller
from backend.src.web_backend.controller import map_controller
from backend.src.web_backend.controller import metrics_controller
from backend.src.web_backend.controller import route_history_controller
from backend.src.web_backend.controller import user_controller

logger = get_logging_configuration()


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)

    setup_tracing("web-backend", True)

    map_controller.init_map_routes(app)
    user_controller.init_user_routes(app)
    route_history_controller.init_path_routes(app)
    health_controller.init_health_routes(app)
    metrics_controller.init_metrics_routes(app)
    return app


def main():
    """Main function to initialize the backend"""
    logger.info("Starting backend application.")
    app = create_app()

    with get_db_session() as db_session:
        fetch_and_store_map_data_if_needed(session=db_session)

    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug_mode, host="0.0.0.0", port=4243)


if __name__ == "__main__":
    main()
