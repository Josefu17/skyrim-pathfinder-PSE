# Group 2 Navigation System

[![Coverage Report](https://code.fbi.h-da.de/bpse-wise2425/group2/badges/main/coverage.svg)](https://code.fbi.h-da.de/bpse-wise2425/group2/-/commits/main)

## Table of Contents
1. [Overview](#overview)  
2. [Core Components](#core-components)  
3. [Getting Started](#getting-started)  
4. [Environment Configuration](#environment-configuration)  
5. [Backend API Overview](#backend-api-overview)  
6. [Database Overview](#database-overview)  
7. [Running the Application](#running-the-application)  
8. [Testing and Code Quality](#testing-and-code-quality)  
9. [Debugging](#debugging)  
10. [Postman Collection](#postman-collection)  
11. [Definition of Done (DoD)](#definition-of-done-dod)  
12. [Requirements Checklist](#requirements-checklist)

---

## Overview

The navigation system calculates and displays optimal routes between cities. It includes:
- **Navigation Service**: Stateless service using Dijkstra's algorithm for route calculations, exposed via an XML-RPC API.
- **Web Backend**: REST API layer interfacing with the navigation service, database, and frontend.
- **Frontend**: UI for map visualization and user interaction.
- **PostgreSQL Database**: Stores city and connection data.

---

## Core Components

### Navigation Service
- Implements route calculation logic.
- Exposed as an XML-RPC API at `http://navigation-service:8000/`.
- Communicates with the web backend to calculate routes using city and connection data.

### Web Backend
- Provides REST endpoints for the frontend.
- Acts as a bridge between the frontend and the navigation service.
- Handles database interactions for fetching/storing map data.

### PostgreSQL Database
- Stores information about cities and their connections.
- Accessed via SQLAlchemy ORM and a DAO pattern.

---

## Getting Started

**Note**: Commands in this documentation use `make` for brevity. Each `make` command corresponds to a specific sequence of actions, detailed in the Makefile.
For more details about the commands, please refer to the said Makefile

### Prerequisites
- **Python** (>= 3.8)
- **pip**
- **Docker & Docker Compose**
- **make** (optional but recommended for ease of use)

### Setup

1. Clone the repository:
   ```bash
   git clone https://code.fbi.h-da.de/bpse-wise2425/group2.git
   cd group2
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
    In case of problems, refer to the official Python [documentation](https://docs.python.org/3/library/venv.html) on virtual environments.

3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt  # Or use `make install`
   ```

[back to top](#table-of-contents)

---

## Environment Configuration

A `.env` file in the root directory is required for local development. Example:

```dotenv
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=<your-db-name>
```

Replace sensitive placeholders with appropriate values. This configuration is used by Docker and the backend.

---

## Backend API Overview

For a more detailed explanation of the API, see the [API Documentation](docs/API.md).

Following is a more concise overview of the API.

### Endpoints

- **`GET /maps`**: Fetch all map data (cities and connections).
- **`GET /cities`**: Fetch city data.
- **`GET /cities/route?startpoint=<city>&endpoint=<city>`**: Calculate the shortest route between two cities.
- **`GET /healthz`**: Check the application's health status.


### Example Workflow
1. Frontend requests a route using `/cities/route`.
2. Web backend fetches data from the database and calls the navigation service.
3. Navigation service calculates the route and returns it to the backend.
4. Backend returns the response to the frontend.

[back to top](#table-of-contents)

---

## Database Overview

### Entities

#### `City`
- Represents a city with `id`, `name`, `position_x`, and `position_y`.

#### `Connection`
- Represents a connection between two cities with `parent_city_id` and `child_city_id`.

#### `Map`
- Contains metadata like `size_x`, `size_y` and `mapname` about a specific map

#### `User`
- Represents a user with their `id` and `username`

### Migrations

Database migrations are managed with **Alembic**. Follow these steps:

### Database Migrations with Alembic

1. **Modify Database Models**  
   Make necessary changes in the database models located under `backend/src/database/schema/`.

2. **Register New Tables**  
   Add new tables to `backend/src/database/models.py`. This file is used to register all database tables.

3. **Generate a New Migration**  
   To create a migration script, temporarily override the `DB_HOST` and `DB_PORT` environment variables so Alembic can connect to the database directly from the host machine:
   ```bash
   DB_HOST=localhost DB_PORT=<your-host-db-port> alembic -c /path/to/alembic.ini --autogenerate -m "Description of migration"
   ```
   - The `DB_HOST` should be `localhost`, and the `DB_PORT` should match the port exposed on the host by `docker-compose` (e.g., `5433`).

4. **Apply Migrations:**  
   Migrations are automatically applied when the backend container starts.

### Database Seeding

To populate the database with dummy data for local development, we provide a seeding script. 
The script inserts sample users and routes into the database.

#### Usage

```bash
# To seed the database
python -m backend.src.database.seed_db seed # or 'make db-seed'

# To clear the database
python -m backend.src.database.seed_db clear # or 'make db-clear'
```

#### Prerequisites
Ensure the database is running (e.g., using Docker Compose):
```bash
docker compose up -d postgres
```

#### `.env` Configuration
The seeding script relies on environment variables for database credentials. Add these to your `.env` file:

**Note**: Ensure the environment variables are set correctly to allow communication with the database from your local machine.

By default:
- `DB_PORT` is set to `5433` (as per the current Docker Compose configuration).
- `DB_HOST` is set to `localhost` for local connections.

If needed, adjust these values to match your setup. Other values:
```dotenv
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_DATABASE=<your_db_name>
```

---

## Running the Application

### Using Docker

1. Build and start all services:
   ```bash
   docker compose up -d  # Or use `make start`
   ```

2. Stop services:
   ```bash
   docker compose down  # Or use `make stop`
   ```

3. Restart services:
   ```bash
   docker compose down && docker compose up -d  # Or use `make restart`
   ```

### Local Development
1. Start the database:
   ```bash
   docker compose up -d postgres
   ```

2. Run the servers locally (in different tabs/terminals):
   - Beforehand, make sure that you adjust the env variables accordingly:
     - DB_PORT to the value exposed by the db container
     - DB_HOST to localhost since local running backend will be communicating with the db via localhost
   
   ```bash
         python -m backend.src.rpc_api.server
      
         python -m backend.src.web_backend.web_backend_controller
   ```
3. Access the application:
   - access the backend via `curl` requests or with the help of a tool like `postman`
   - example curl commands:
     - `curl -X GET http://localhost:4243/maps`
     - `curl -X GET http://localhost:4243/cities`
   - For our postman collection, please refer to [Postman Collection](docs/Postman/PSE.postman_collection.json)
   or [Documentation.](#postman-collection)

[back to top](#table-of-contents)

---

## Testing and Code Quality

### Testing and Coverage

Run tests locally:
```bash
python -m pytest backend/src/tests/  # Or use `make test`
```

Generate and view a coverage report:
```bash
# Or use `make coverage`
pytest --cov=backend/src --cov-report=html:backend/htmlcov backend/src/tests/  


xdg-open backend/htmlcov/index.html  # Open coverage report (Linux)
start backend\htmlcov\index.html  # Open coverage report (Windows)
```
### Linting and Formatting
The pipeline enforces code quality using Pylint (linter) and Black (formatter). Both are applied to all Python files in
the `src` directory, and the pipeline fails if the code does not meet the required standards.

- **Linter**: `pylint`
- **Formatter**: `black`

Run linting:
```bash
pylint backend/src/**/*.py --rcfile=backend/.pylintrc # Or use `make lint`
```

Run formatting:
```bash
black backend/src/**/*.py --config backend/pyproject.toml # Or use `make format`
```

### Code Analysis with SonarQube
The **SonarQube** integration ensures continuous static code analysis to maintain high code quality and security 
standards. It is integrated both in the CI pipeline and for local usage.

- **Static Code Analysis**: Run with [SonarCloud](https://sonarcloud.io/) for code quality checks, including identifying
code smells, bugs, and security vulnerabilities.
- **Configuration**: The analysis is automatically triggered in the pipeline for each branch. For details on local usage
and advanced setup, refer to [Static Code Analysis Documentation](docs/DevExp.md#static-code-analysis-sonarqube).

[back to top](#table-of-contents)

---

## Debugging

We use `debugpy` for debugging. For configuration instructions, please refer to the [Debugger documentation](docs/DevExp.md#debugger-debugpy).

---

## Postman Collection

A Postman collection is available under the `docs/Postman` directory to test the API endpoints quickly and easily. The collection includes:
- **Maps Endpoint**: Fetch map data.
- **Cities Endpoint**: Fetch city data.
- **Route Calculation**: Example for calculating a route between `Whiterun` and `Riften`.
- **Health Check**: Verify the application's health.

To use the collection, import the file into Postman. Ensure the `base_url` variable matches your local or deployed backend.

## Definition of Done (DoD)

A task or feature is complete when it fulfills requirements for code quality, testing, functionality, and collaboration.  
For detailed criteria, kindly refer to the [DoD Documentation](docs/DoD.md).

---

## Requirements Checklist

Dear lecturers, as much as we tried to keep our README realistic, we wanted to make life a bit easier for you during 
the evaluation. We provide detailed checklists for individual stages, referencing specific documentation where 
requirements are addressed. 

[Requirement Checklists](docs/Stages/stages_overview.md)

---

[back to top](#table-of-contents)
