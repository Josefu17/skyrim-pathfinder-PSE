# DevExp

This document focuses on the developer experience, covering setup processes, debugging tools, one-click commands for 
installation and application startup, and automated dependency updates. It aims to simplify development workflows and 
enforce consistent practices.

---

## Table of Contents
1. [Debugger (debugpy)](#debugger-debugpy)
2. [One-Click installation](#one-click-installation)
3. [One-Click Start for the Application (localdev)](#one-click-start-for-the-application-localdev)
4. [Tests run locally and in CI](#tests-run-locally-and-in-ci)
5. [Linter and Formatter Setup](#linter-and-formatter-setup)
6. [Project's setup process and major design decisions](#projects-setup-process-and-major-design-decisions)

## Debugger (debugpy)
- Add debugpy to requirements.txt
- Each Python service has the following entry under `ports`:
```yaml
ports:
 - "5678:5678"
```
This maps the container's debugpy port (`5678`) to the host machine, enabling remote debugging.


#### Setup for Vs Code
Create a file .vscode/launch.json in the root directory.

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Remote Attach",
      "type": "debugpy",
      "request": "attach",
      "connect": {
        "host": "localhost",
        "port": 5678
      },
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}/src",
          "remoteRoot": "/app/src"
        }
      ]
    }
  ]
}

```
Remote Attach: so that VS Code can attach to a running Python application on a remote system

#### Setup for PyCharm

**Configure the Python Interpreter**
1. Navigate to **File > Settings**.
2. Select **Project: *project_name***.
3. Click on **Python Interpreter** and then **Add Interpreter**.
4. Choose **Docker-Compose** as the interpreter type.
5. Set the **Service** to `web-backend` and confirm with **Apply**.

**Create a Run/Debug Configuration**
1. Navigate to **Run > Edit Configuration**.
2. Click on the **plus icon** and select **Python** as the configuration type.
3. Set the **Interpreter** to the previously configured remote debugger.
4. Select `web_backend_controller.py` as the **Script**.
5. Specify the path to the `.env` file to ensure environment variables are loaded correctly, and confirm with **Apply**.

[back to top](#devexp)

## One-Click installation
### Installation and Removal of Dependencies
Two targets have been added to the ``Makefile``: ``install`` and ``remove``. Depending on the command, they install
or remove the dependencies.

### Usage
To install the dependencies, run the following command from the root folder:
```
make install
```
To remove the dependencies, run:
```
make remove
```
These commands provide a "one-click" solution for managing dependencies, ensuring a clean environment.

[back to top](#devexp)

## One-Click Start for the Application (localdev)

The application can be started locally with a single command using the `Makefile`. This command initializes all services
(Postgres, Navigation Service, Web Backend) defined in the `docker-compose.yml` file.

### Prerequisites
1. Ensure you have Docker and Docker Compose installed on your machine.
2. Verify that the `Makefile` and `docker-compose.yml` files are in the root directory of your project.

### Steps to Start
1. Open a terminal and navigate to the project's root directory.
2. Run the following command:
   ```bash
   make start
   ```

   This will:
   - Build and start the services defined in the `docker-compose.yml` file in detached mode.
   - Ensure the application is running locally on the configured ports.

### Accessing the Services
- **Navigation Service**:  
  Accessible at [http://localhost:8000](http://localhost:8000).
- **Web Backend**:  
  Accessible at [http://localhost:5000](http://localhost:5000).
- **Postgres Database**:  
  Use `make connect-to-database` to access the database directly:
  ```bash
  make connect-to-database
  ```

### Stopping the Application
To stop the application and remove all containers, run:
```bash
make stop
```


[back to top](#devexp)

## Tests run locally and in CI

With `pytest`, we have created tests for our features that can be run locally. In the CI, they run in the 'test-job'. 
Python files starting with 'test' are executed with `python -m pytest`.

From the root folder:
```
script:
    pytest ./backend/src/tests # or use `make test`
    # with coverage:
    pytest --cov=backend/src --cov-report=html:backend/htmlcov 
        backend/src/tests/ --cov-config=backend/setup.cfg # or use `make coverage`

```

## Automated Dependency Updates with Renovate

We use **Renovate** to automate dependency updates, ensuring our project stays secure and up-to-date with minimal 
effort. Renovate scans our project for outdated dependencies and creates merge requests (MRs) with the necessary updates.

### Key Features
- **Automatic Updates**: Checks `requirements.txt` and `pyproject.toml` for outdated packages.
- **Merge Requests**: Creates MRs for each update with changelogs when available.
- **Customizable**: Configuration in `renovate.json` allows grouping updates (e.g., minor/major) and setting automerge rules.

### Workflow
1. **MR Creation**: Renovate opens MRs with dependency updates.
2. **Review and Testing**: Review the MR changelog and ensure the pipeline passes, make additional checks like running
the application locally and testing if things are working depending on the change from Renovate.
3. **Merge**: Merge the MR to apply updates.

---

## Linter and Formatter Setup

We use:
- **Linter**: `pylint` (configuration in `.pylintrc`)
- **Formatter**: `black` (configuration in `pyproject.toml`)

Both tools are configured to run locally and in the CI pipeline with the same settings to ensure consistent code quality.

For more detail on those, please refer to [here.](../README.md#linting-and-formatting)

---

### Local Setup

1. **Install Dependencies**:
   Use the `Makefile`:
   ```bash
   make install
   ```

2. **Run Linter and Formatter**:
   ```bash
   python -m pylint --rcfile=backend/.pylintrc src/*.py # or use `make lint`
   python -m black --config pyproject.toml src/*.py # or use `make format`
   ```

---

### CI Pipeline

1. **Install Dependencies**:
   The `analyze-job` in the CI pipeline installs the tools:
   ```yaml
   before_script:
     - pip install -r backend/requirements.txt
   ```

2. **Run Linter and Formatter**:
   The CI pipeline validates code with:
   ```yaml
   script:
     - python -m pylint --rcfile=backend/.pylintrc src/*.py
     - python -m black --config backend/pyproject.toml src/*.py
   ```

---

### Ensuring Consistency
- **Single Source of Truth**: The `.pylintrc` and `pyproject.toml` files ensure consistent rules across all environments.
  - A note on this: Our configuration files are either pretty much the same as the default or contain minimal differences / configurations,
  we still decided to generate and specify the configuration files explicitly to enforce consistency between local 
  development and CI Pipeline.

[back to top](#devexp)

## Project's setup process and major design decisions

### Setup Process  
To simplify the setup process for developers, we created a `Makefile` with commands for installing dependencies 
(`make install`), starting services (`make start`), and cleaning the environment (`make remove`). This ensures a 
consistent setup process across different development environments. We use Python virtual environments for local 
development, while Docker Compose manages dependencies like the PostgreSQL database.

Debugging is enabled using `debugpy`, with configurations provided for both PyCharm and VS Code. This allows developers 
to debug containerized services seamlessly by attaching their IDE to the running services.
---
### Major Design Decisions  
**Architecture:** The project follows a microservices architecture to separate concerns. The Navigation Service is stateless and uses 
Dijkstra's algorithm to calculate routes, exposed via an XML-RPC API. The Web Backend serves as a REST API layer that 
interfaces with the database and frontend. This separation allows for independent scaling and modular development.

**DB Choice and Migrations:** PostgreSQL was chosen for its reliability and compatibility with spatial data. SQLAlchemy provides ORM capabilities, 
and Alembic is used for managing database migrations. These tools ensure schema consistency and ease of schema evolution.

**Code Quality:** To enforce code quality, we integrated `pylint` and `black`, with configurations consistent across local development 
and the CI pipeline. All tests are written using pytest and are executed locally and in the CI pipeline to catch issues early.
