# Group 2 Navigation System

A small web application that calculates and displays optimal routes between cities on a map.  
It combines a stateless navigation service (Dijkstra’s algorithm), a REST backend, a web UI, and a PostgreSQL database.

This project was developed in winter 2024 as part of the **“Projektsystementwicklung (PSE)”** course at  
**Hochschule Darmstadt**, where we designed, implemented, deployed, and maintained the app end-to-end  
(including tests, CI pipeline, and monitoring).

---

## Project Status

This is an educational university project built for a single semester.  
It is not actively maintained and serves primarily as a demonstration of architecture, testing, and DevOps practices.

---

## Tech Stack

**Backend & Navigation Service**

- Python (3.8+)
- Stateless Navigation Service using Dijkstra’s algorithm
- XML-RPC for communication with the navigation service
- REST web backend (Python, SQLAlchemy, DAO pattern)
- PostgreSQL with Alembic for migrations

**Frontend**

- Vanilla JavaScript, HTML, CSS
- Interactive map visualization and route display

**Infrastructure & Tooling**

- Docker & Docker Compose
- Prometheus & Grafana for monitoring and metrics
- Pytest for tests & coverage
- Black & Pylint for formatting and linting
- SonarCloud / SonarQube for static code analysis
- Makefile for common development and CI tasks

---

## Architecture & Main Features

The system is split into several components:

- **Stateless Navigation Service**
  - Implements Dijkstra’s algorithm to calculate shortest and alternative routes.
  - Exposed via XML-RPC as a separate service.

- **Web Backend**
  - Provides REST endpoints for the frontend and external tools (e.g. Postman).
  - Orchestrates calls to the navigation service and the database.
  - Exposes health and metrics endpoints for monitoring.

- **PostgreSQL Database**
  - Stores cities, connections, maps, users, and route history.
  - Managed via Alembic migrations and seeding scripts for local development.

- **Frontend**
  - Displays the map, cities, and connections.
  - Lets users select start and end cities to calculate routes.
  - Shows the optimal and alternative routes and their distances.
  - Provides basic user management (register/login) and route history.

- **Monitoring & Observability**
  - Metrics for latency, traffic, errors, and saturation.
  - Integration with Prometheus and Grafana dashboards.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Docker & Docker Compose
- `make` (optional, but handy for common tasks)
- A `.env` file with database connection details (e.g. `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_DATABASE`)

### Quick Start (Docker)

1. Clone the repository:

   ```bash
   git clone <this-repo-url>
   cd group2-navigation-system
````

2. Create a `.env` file in the project root and fill in the required `DB_*` variables
   (see the example in the repository or `docker-compose.yml` for reference).

3. Start all services:

   ```bash
   docker compose up -d
   # or, if available:
   make start
   ```

4. Open the ports defined in `docker-compose.yml` in your browser
   (backend and, if configured, frontend).

To work on individual components locally (without Docker), you can run the navigation service and web backend
as Python modules and point them to your local PostgreSQL instance. See the project’s documentation and dev
files (`docs/`, `backend/`) for details.

---

## Testing & Code Quality

* **Tests & Coverage**

  * Python tests implemented with `pytest`.
  * Coverage reports for the backend.

* **Linting & Formatting**

  * `black` for formatting.
  * `pylint` for linting.

* **Static Code Analysis**

  * Integrated with SonarCloud / SonarQube for additional quality and security checks.
  * Run automatically in the CI pipeline.

---

## Team

Developed collaboratively as part of the PSE course at Hochschule Darmstadt. Developers:

- **Arian Farzad**
- **Târik-Cemal Atis**
- **Yusuf Birdane**