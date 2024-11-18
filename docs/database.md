# Database Documentation

## Overview
This document outlines the structure and configuration of the PostgreSQL database used in our project. It also describes how we manage database interactions using SQLAlchemy ORM and the DAO (Data Access Object) pattern.

---

### Database Configuration
- **Containerized PostgreSQL**: We use a Dockerized Postgres instance configured via `docker-compose.yml`.  
- **Environment Variables**: Credentials and database details are defined in a `.env` file (not included in version control). 

#### Start the Database
```bash
docker-compose up -d
```

#### Access the Database
- **Command Line**:  
  ```bash
  docker exec -it <container-name> psql -U <POSTGRES_USER> -d <POSTGRES_DB>
  ```
- **pgAdmin**: Configure a new server connection with:
  - Host: `localhost`
  - Port: `5432`
  - Maintenance Database: `<POSTGRES_DB>`
  - Username/Password: Refer to `.env`

---

### ORM Integration
- **Framework**: SQLAlchemy is used to handle database interactions.  
- **Behavior**:
  - Automatically checks for database existence.
  - Creates missing databases or tables based on schema definitions.  
  - Facilitates easy database interaction via the DAO pattern.

---

### Key Concepts
- **Schema Definitions**:  
  The schema (e.g., `City`, `Connection` tables) is defined in the ORM models. Refer to the `src.database.schema` module for detailed implementation.
- **DAO Pattern**:  
  Data access logic is encapsulated in `CityDAO` and `ConnectionDAO`, which provide methods to query and manipulate the database. Refer to `src.database.dao` for usage details.

---

## Notes
- **Environment Variables**: Credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) are managed through a `.env` file to avoid exposing sensitive information in the source code.  
- **Error Handling**: The DAO methods include basic error handling for robustness.  
