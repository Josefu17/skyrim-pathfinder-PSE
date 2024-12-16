# Make Targets' Documentation

This document provides a complete overview of all available `make` targets in this repository, including descriptions, usage, and additional notes.

---

## **Table of Contents**

1. [General Targets](#general-targets)
   - [Help](#help)
2. [Dependency Management](#dependency-management)
   - [Install](#install)
   - [Remove](#remove)
3. [Docker Management](#docker-management)
   - [Build](#build)
   - [Build-CI](#build-ci)
   - [Push](#push)
   - [Start](#start)
   - [Start-Frontend](#start-frontend)
   - [Stop](#stop)
   - [Restart](#restart)
   - [Login](#login)
   - [Update](#update)
4. [Testing and Coverage](#testing-and-coverage)
   - [Test-Backend](#test-backend)
   - [Test-Frontend](#test-frontend)
   - [Test](#test)
   - [Coverage-Backend](#coverage-backend)
   - [Coverage-Frontend](#coverage-frontend)
   - [Coverage](#coverage)
   - [Coverage-Open-Windows](#coverage-open-windows)
   - [PS-Coverage-Backend](#ps-coverage-backend)
   - [PS-Coverage-Frontend](#ps-coverage-frontend)
   - [PowerShell-Coverage](#ps-coverage)
   - [Coverage-Open-Unix](#coverage-open-unix)
5. [SonarQube Management](#sonarqube-management)
   - [Sonar](#sonar)
6. [Code Quality](#code-quality)
   - [Lint-Backend](#lint-backend)
   - [Lint-Frontend](#lint-frontend)
   - [Lint](#lint)
   - [Format-Backend](#format-backend)
   - [Format-Frontend](#format-frontend)
   - [Format](#format)
7. [Pre-Commit Check](#pre-commit-check)
   - [Pre-Commit-Backend](#pre-commit-backend)
   - [Pre-Commit-Frontend](#pre-commit-frontend)
   - [Pre-Commit](#pre-commit)
8. [Service Management](#service-management)
   - [Navigation-Service-Enter](#nav-enter)
   - [Backend-Service-Enter](#backend-enter)
9. [Database Management](#database-management)
   - [Migrate](#migrate)
   - [Connect-to-Database](#connect-to-database)
10. [NPM Management](#npm-management)
    - [Run NPM Scripts](#run-npm-scripts)
    - [Start Frontend Development Mode](#dev)

---

## **General Targets**

### `help`
Displays a list of all available `make` targets with a brief description.

[Back to Top](#make-targets-documentation)

---

## **Dependency Management**

### `install`
Installs all required dependencies:
- Backend: `pip install -r backend/requirements.txt`
- Frontend: `npm ci` in the `frontend` directory.

[Back to Top](#make-targets-documentation)

---

### `remove`
Removes all dependencies:
- Backend: `pip uninstall -r backend/requirements.txt`
- Frontend: `npm uninstall`.

[Back to Top](#make-targets-documentation)

---

## **Docker Management**

### `build`
Builds Docker images for:
- `web-frontend` (tagged as `latest` locally).
- All other services via `docker-compose build`.

[Back to Top](#make-targets-documentation)

---

### `build-ci`
Builds Docker images for CI/CD:
- `web-frontend`
- `navigation-service`
- `web-backend`

[Back to Top](#make-targets-documentation)

---

### `push`
Pushes all Docker images to the Docker registry `registry.code.fbi.h-da.de`.

[Back to Top](#make-targets-documentation)

---

### `start`
Starts the entire Docker environment:
- Builds Docker images (if necessary).
- Runs `docker compose up -d`.
- Starts the frontend development environment with `make dev`.

[Back to Top](#make-targets-documentation)

---

### `start-frontend`
Builds the `web-frontend` image and starts it as a standalone container on port `4242`.

[Back to Top](#make-targets-documentation)

---

### `stop`
Stops all running containers and removes the entire Docker environment using `docker compose down`.

[Back to Top](#make-targets-documentation)

---

### `restart`
Combination of `stop` and `start`.

[Back to Top](#make-targets-documentation)

---

### `login`
Logs in to the Docker registry at `registry.code.fbi.h-da.de` using Docker's CLI. This step is required before pushing or pulling Docker images to/from the registry.

[Back to Top](#make-targets-documentation)

---

### `update`
Logs into the Docker registry, builds the images, and pushes them.

[Back to Top](#make-targets-documentation)

---

## **Testing and Coverage**

### `test-backend`
Runs all backend tests with `pytest` in the `backend/src/tests/` directory.

[Back to Top](#make-targets-documentation)

---

### `test-frontend`
Runs frontend tests with `npm run test`.

[Back to Top](#make-targets-documentation)

---

### `test`
Runs both `test-backend` and `test-frontend`.

[Back to Top](#make-targets-documentation)

---

### `coverage-backend`
Generates coverage reports for the backend:
- Backend: HTML and XML reports in `backend/coverage-reports`.

[Back to Top](#make-targets-documentation)

---

### `coverage-frontend`
Generates coverage reports for the frontend:
- Frontend: Coverage reports in `frontend/coverage`.

[Back to Top](#make-targets-documentation)

---

### `coverage`
Generates both backend and frontend coverage reports.

[Back to Top](#make-targets-documentation)

---

### `coverage-open-windows`
Generates the coverage report and opens the HTML report in the browser on Windows.

[Back to Top](#make-targets-documentation)

---

### `ps-coverage-backend`
Generates the backend coverage report and opens it in the browser using PowerShell.

[Back to Top](#make-targets-documentation)

---

### `ps-coverage-frontend`
Generates the frontend coverage report and opens it in the browser using PowerShell.

[Back to Top](#make-targets-documentation)

---

### `ps-coverage`
Generates both backend and frontend coverage reports and opens them in the browser using PowerShell.

[Back to Top](#make-targets-documentation)

---

### `coverage-open-unix`
Generates the coverage report and opens it in the browser on Unix-based systems using `xdg-open`.

[Back to Top](#make-targets-documentation)

---

## **SonarQube Management**

### `sonar`
Runs SonarQube analysis. Before running SonarQube, it generates the coverage report as a prerequisite.

[Back to Top](#make-targets-documentation)

---

## **Code Quality**

### `lint-backend`
Checks the backend code for linting issues using `pylint` with the configuration file `backend/.pylintrc`. Also triggers the frontend linting via the `npm` target.

[Back to Top](#make-targets-documentation)

---

### `lint-frontend`
Checks the frontend code for linting issues using `eslint` via `npm run lint`.

[Back to Top](#make-targets-documentation)

---

### `lint`
Runs both backend and frontend linting.

[Back to Top](#make-targets-documentation)

---

### `format-backend`
Formats the backend code using `black` with the configuration file `backend/pyproject.toml`.

[Back to Top](#make-targets-documentation)

---

### `format-frontend`
Formats the frontend code using Prettier.

[Back to Top](#make-targets-documentation)

---

### `format`
Formats both backend and frontend code.

[Back to Top](#make-targets-documentation)

---

## **Pre-Commit Check**

### `pre-commit-backend`
Runs the backend pre-commit checks:
- Tests
- Format
- Lint
- Coverage

[Back to Top](#make-targets-documentation)

---

### `pre-commit-frontend`
Runs the frontend pre-commit checks:
- Tests
- Format
- Lint
- Coverage

[Back to Top](#make-targets-documentation)

---

### `pre-commit`
Runs both backend and frontend pre-commit checks.

[Back to Top](#make-targets-documentation)

---

## **Service Management**

### `nav-enter`
Provides an interactive shell inside the running navigation service container.

[Back to Top](#make-targets-documentation)

---

### `backend-enter`
Provides an interactive shell inside the running backend service container.

[Back to Top](#make-targets-documentation)

---

## **Database Management**

### `migrate`
Applies all database migrations using Alembic, with the configuration provided in `backend/alembic.ini`.

[Back to Top](#make-targets-documentation)

---

### `connect-to-database`
Connects to the running PostgreSQL database container (`group2-postgres-1`) using `psql`.

[Back to Top](#make-targets-documentation)

---

## **NPM Management**

### `run-npm-scripts`
Runs an npm script defined in the `frontend/package.json`. The script to run is provided by setting the `run` variable.

[Back to Top](#make-targets-documentation)

---

### `dev`
Starts the frontend development mode by running `npm run dev` in the `frontend` directory.

[Back to Top](#make-targets-documentation)

---
