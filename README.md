# Group 2 Navigation System

A small web application that calculates and displays optimal routes between cities on a map.  
It combines a stateless navigation service (Dijkstra’s algorithm), a REST backend, a web UI, and a PostgreSQL database.

This project was developed in winter 2024 as part of the **“Projektsystementwicklung (PSE)”** course at  
**Hochschule Darmstadt**, where we designed, implemented, deployed, and maintained the app end-to-end  
(including tests, CI pipeline, and monitoring).

---

## Project Status

This is an educational, one-semester university project.  
It is **not actively maintained** and is mainly published for portfolio / reference purposes.  
The Docker setup is sufficient to spin up the stack locally for screenshots and code exploration.

---

## Tech Stack

**Backend & Navigation Service**

- Python (3.8+)
- Flask, SQLAlchemy, DAO pattern
- Stateless navigation service using Dijkstra’s algorithm (XML-RPC)
- PostgreSQL with Alembic migrations

**Frontend**

- React with Vite
- TypeScript
- HTML & CSS for layout and styling
- Map visualization and route display

**Infrastructure & Tooling**

- Docker & Docker Compose
- Prometheus & Grafana (monitoring / metrics)
- Pytest, Black, Pylint
- SonarCloud / SonarQube
- Makefile for common dev/CI tasks

---

## Architecture & Features

- **Navigation Service**
    - Calculates shortest and alternative routes using Dijkstra’s algorithm.
    - Exposed as a separate XML-RPC service.

- **Web Backend (REST API)**
    - Bridges frontend, navigation service, and database.
    - Exposes endpoints for maps, cities, route calculation, users, health, and metrics.

- **Database (PostgreSQL)**
    - Stores cities, connections, maps, users, and route history.
    - Managed via Alembic with migrations and seeding support.

- **Frontend**
    - Displays maps, cities, and connections.
    - Lets users select start and end cities, view routes, and inspect route history.
    - Basic user registration and login.

- **Dummy Maps (public version)**
    - The original project used an internal university map service.
    - In this public version, the backend generates a few dummy maps locally on startup
      (e.g. `Dummy-10x10`, `Dummy-25x25`, …) and stores them in the DB.

---

## Getting Started

### Prerequisites

- Docker & Docker Compose

(Optional: Python 3.8+ if you want to poke at backend services without Docker.)

---

### Environment Configuration

The root folder contains an `.env.template` for local development.

1. Copy it to `.env`:

   ```bash
   cp .env.template .env
   ```

2. Adjust the values if needed.
   The default settings are enough for a standard local Docker setup.

---

### Quick Start (Docker)

From the project root:

```bash
docker compose up -d --build
```

Then open:

* **Frontend:** [http://localhost:4242](http://localhost:4242)
* **Backend API:** [http://localhost:4243](http://localhost:4243)

To stop everything:

```bash
docker compose down
```

To reset the database as well:

```bash
docker compose down -v
```

---

## Testing & Code Quality

* Backend tests written with **pytest** (see `backend/`).
* Code style enforced via **Black** and **Pylint**.
* Static analysis integrated with **SonarCloud / SonarQube** in the original CI pipeline.

---

## Team

Developed collaboratively as part of the PSE course at Hochschule Darmstadt:

- **Arian Farzad**: Backend  (API, tests), Navigation Service
- **Yusuf Birdane**: Backend (API, tests), Database Setup and migrations.
- **Târik-Cemal Atis**: Frontend Development
