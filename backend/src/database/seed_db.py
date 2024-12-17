"""Python file to seed the local db with some dummy data"""

import os
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from backend.src.database.schema.models import register_models
from backend.src.database.schema.route import Route
from backend.src.database.schema.user import User
from backend.src.utils.helpers import load_dotenv_if_exists

register_models()

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv_if_exists(dotenv_path)


# Database credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"  # Localhost for host connection
DB_PORT = "5433"  # Port mapped for host according to the docker-compose file, modify if necessary
DB_DATABASE = os.getenv("DB_DATABASE")

# Routes to be seeded
ROUTE_DATA = [
    (
        "Markarth",
        "Karthwasten",
        {
            "alternative_distance": 919.07,
            "alternative_route": {"0": "Markarth", "1": "Rorikstead", "2": "Karthwasten"},
            "distance": 321.12,
            "route": {"0": "Markarth", "1": "Karthwasten"},
        },
    ),
    (
        "Karthwasten",
        "Helgen",
        {
            "alternative_distance": 1452.31,
            "alternative_route": {
                "0": "Karthwasten",
                "1": "Rorikstead",
                "2": "Whiterun",
                "3": "Riverwood",
                "4": "Helgen",
            },
            "distance": 1339.61,
            "route": {"0": "Karthwasten", "1": "Rorikstead", "2": "Falkreath", "3": "Helgen"},
        },
    ),
    (
        "Riften",
        "Dawnstar",
        {
            "alternative_distance": 2243.13,
            "alternative_route": {
                "0": "Riften",
                "1": "Shor’s Stone",
                "2": "Windhelm",
                "3": "Winterhold",
                "4": "Dawnstar",
            },
            "distance": 1790.23,
            "route": {
                "0": "Riften",
                "1": "Shor’s Stone",
                "2": "Windhelm",
                "3": "Winterhold",
                "4": "Dawnstar",
            },
        },
    ),
    (
        "Ivarstead",
        "Falkreath",
        {
            "alternative_distance": 1012.5,
            "alternative_route": {
                "0": "Ivarstead",
                "1": "Helgen",
                "2": "Riverwood",
                "3": "Falkreath",
            },
            "distance": 677.05,
            "route": {"0": "Ivarstead", "1": "Helgen", "2": "Falkreath"},
        },
    ),
]

# Database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# Setup SQLAlchemy
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def seed_data():
    """Populate the database with dummy users and routes."""
    session = Session()
    print("Seeding data...")

    try:
        # Clear existing data
        session.query(Route).delete()
        session.query(User).delete()
        session.commit()

        # Create dummy users
        users = [User(username="user1"), User(username="user2"), User(username="user3")]
        session.add_all(users)
        session.commit()
        print("Added dummy users.")

        # Fetch users
        user_ids = [user_id for (user_id,) in session.query(User).with_entities(User.id).all()]

        # Add routes for each user
        now = datetime.now(timezone.utc)
        routes = []
        for user_id in user_ids:
            for startpoint, endpoint, route_data in ROUTE_DATA:
                days_offset = secrets.randbelow(31)  # Random number from 0 to 30
                created_at = now - timedelta(days=days_offset)
                route = Route(
                    user_id=user_id,
                    startpoint=startpoint,
                    endpoint=endpoint,
                    created_at=created_at,
                    route=route_data,
                )
                routes.append(route)

        session.add_all(routes)
        session.commit()
        print("Added dummy routes.")

    except SQLAlchemyError as e:
        print(f"Database error while seeding data: {e}")
        session.rollback()
    finally:
        session.close()
        print("Seeding completed.")


def clear_data():
    """Clear all seeded data from users and routes."""
    session = Session()
    print("Clearing data...")

    try:
        session.query(Route).delete()
        session.query(User).delete()
        session.commit()
        print("Data cleared successfully.")
    except SQLAlchemyError as e:
        print(f"Database error while clearing data: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed or Clear Database Data")
    parser.add_argument(
        "action", choices=["seed", "clear"], help="Action to perform: seed data or clear data."
    )
    args = parser.parse_args()

    if args.action == "seed":
        seed_data()
    elif args.action == "clear":
        clear_data()
