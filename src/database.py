"""
ORM Behavior for Database Management:

Check for Database Existence: The ORM first checks whether the specified database already exists.

Database Connection:

If the database exists:
  The ORM establishes a connection to the existing database.
If the database does not exist:
  The ORM creates the required database and then establishes the connection.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
import requests
from tables import Cities, Connections, Base


USER = "pg-2"
PASSWORD = "pg-2"
HOST = "postgres"
PORT = "5432"
DB_NAME = "navigation"


engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/postgres"
)


with engine.connect() as connection:
    try:
        result = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": DB_NAME},
        )
        exists = result.fetchone() is not None

        if not exists:
            connection.execute(text(f"CREATE DATABASE {DB_NAME};"))
            print(f"Database '{DB_NAME}' created.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

    except ProgrammingError as e:
        print(f"Error: {e}")
        raise


new_engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
)


with new_engine.connect() as new_connection:
    try:
        Base.metadata.create_all(new_engine)
        print("Tables created")
    except ProgrammingError as e:
        print(f"Error creating tables: {e}")


SESSION_MAKER = sessionmaker(bind=new_engine)
SESSION = SESSION_MAKER()

URL = "https://maps.proxy.devops-pse.users.h-da.cloud/map?name=skyrim"
try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    city_map = {}

    for city in data["cities"]:
        db_city = SESSION.query(Cities).filter_by(name=city["name"]).first()
        if not db_city:
            db_city = Cities(
                name=city["name"],
                position_x=city["positionX"],
                position_y=city["positionY"],
            )
            SESSION.add(db_city)
            SESSION.commit()
            print(f"City { city['name'] } added")
        city_map[city["name"]] = db_city.id

    for connection in data["connections"]:
        parent_city_id = city_map.get(connection["parent"])
        child_city_id = city_map.get(connection["child"])

        if parent_city_id and child_city_id:
            db_connection = (
                SESSION.query(Connections)
                .filter_by(parent_city_id=parent_city_id, child_city_id=child_city_id)
                .first()
            )
        if not db_connection:
            db_connection = Connections(
                parent_city_id=parent_city_id, child_city_id=child_city_id
            )
            SESSION.add(db_connection)
            print(
                f"Connection from { connection['parent'] } to { connection['child'] } added"
            )

    SESSION.commit()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
