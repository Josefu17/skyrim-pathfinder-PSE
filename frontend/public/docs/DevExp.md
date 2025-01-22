# DevExp

This document focuses on the developer experience, covering setup processes, debugging tools, one-click commands for
installation and application startup, and automated dependency updates. It aims to simplify development workflows and
enforce consistent practices.

---

## **Table of Contents**

1. [Debugger (debugpy)](#debugger-debugpy)

    - Quick setup for remote debugging with VS Code and PyCharm

2. [One-Click Installation](#one-click-installation)

    - Managing dependencies (install/remove) via Makefile

3. [One-Click Start for the Application (localdev)](#one-click-start-for-the-application-localdev)

    - Prerequisites for Docker and Makefile
    - Starting and stopping all services with a single command

4. [Tests Run Locally and in CI](#tests-run-locally-and-in-ci)

    - Running `pytest` locally and in CI pipelines
    - Coverage reports for Python tests

5. [Automated Dependency Updates with Renovate](#automated-dependency-updates-with-renovate)

    - MR workflows for dependency updates
    - Grouping updates by type (e.g., minor, major)

6. [Linter and Formatter Setup](#linter-and-formatter-setup)

    - Local setup and running `pylint`/`black`
    - Integrating linting/formatting in CI pipelines

7. [Static Code Analysis (SonarQube)](#static-code-analysis-sonarqube)

    - Local setup for Windows/Linux with SonarScanner
    - IDE integration (VS Code and PyCharm)
    - Configuration for SonarCloud in CI

8. [Project Setup Process and Major Design Decisions](#projects-setup-process-and-major-design-decisions)
    - Simplified environment setup with Makefile and Docker Compose
    - Key architectural choices (e.g., microservices, PostgreSQL)
    - Debugging tools and schema migration setup

---

## Debugger (debugpy)

- Add debugpy to requirements.txt
- Each Python service has the following entry under `ports`:

```yaml
ports:
    - '5678:5678'
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
2. Select **Project: _project_name_**.
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

Two targets have been added to the `Makefile`: `install` and `remove`. Depending on the command, they install
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

- **Linter**:
    - `pylint` (configuration in `.pylintrc`)
    - `ESLint` (configuration in `.eslintrc.js`)
- **Formatter**:
    - `black` (configuration in `pyproject.toml`)
    - `Prettier` (configurations in `.prettierrc` and `.prettierignore`)

`pylint` and `black` are configured to run locally and in the CI pipeline with the same settings to ensure consistent code quality.
`ESLint` and `Prettier` have yet to get set up in the Ci pipeline.

For more detail on those, please refer to [here.](../README.md#linting-and-formatting)

---

### Local Setup

1. **Install Dependencies**:
   Use the `Makefile`:

    ```bash
    make install
    ```

2. **Run Linter and Formatter**:
   for Python and TypeScript:

    ```bash
    make lint
    make format
    ```

    for Python only:

    ```bash
    python -m pylint --rcfile=backend/.pylintrc src/*.py
    python -m black --config pyproject.toml src/*.py
    ```

    for TypeScript only:

    ```bash
    make npm run=lint
    make npm run=format
    ```

3. **Run Inside Docker**:
    ```bash
    docker exec -it <container-name> sh -c "
       python -m pylint --rcfile=backend/.pylintrc src/*.py &&
       python -m black --config backend/pyproject.toml src/*.py
    "
    ```

---

### Linting and formatting in the CI Pipeline

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

## **Static Code Analysis (SonarQube)**

### **Overview**

SonarQube ensures adherence to code quality standards both locally and in CI. This section covers local setups for
Windows and Linux, IDE integrations, and configuration in CI pipelines.

---

### **1. Local Setup**

SonarScanner can be run locally for analysis before pushing changes.

#### **For Windows**

1. Download and extract [SonarScanner](https://docs.sonarsource.com/sonarqube-server/9.9/analyzing-source-code/scanners/sonarscanner/).
2. Add the `bin` directory to your system’s `PATH` environment variable.

    Example:

    ```powershell
    setx PATH "%PATH%;C:\path\to\sonar-scanner\bin"
    ```

3. Set the `SONAR_TOKEN` (authentication):

    - **Per Session (Temporary)**:
        ```powershell
        set SONAR_TOKEN=<your_sonar_token>
        ```
    - **Global Setup (Persistent)**:  
      Edit the scanner properties file at:
        ```plaintext
        <INSTALL_DIRECTORY>\conf\sonar-scanner.properties
        ```
        Add this line:
        ```plaintext
        sonar.token=<your_sonar_token>
        ```

4. Generate a test Coverage report in XML format:

    ```bash
      	python -m pytest --cov=backend/src --cov-config=backend/setup.cfg --cov-report=xml:backend/coverage-reports/coverage.xml backend/src/tests/
        # or run make coverage
    ```

5. Run the scanner:
    ```bash
    sonar-scanner
    ```

**Tip:** Steps **4** & **5** can be streamlined with the make target `make sonar`

---

#### **For Linux/Unix**

1. Download and install SonarScanner:

    ```bash
    mkdir -p ~/.sonar
    curl -sSLo ~/.sonar/sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-6.2.1.4610-linux.zip
    unzip ~/.sonar/sonar-scanner.zip -d ~/.sonar/
    export PATH=~/.sonar/sonar-scanner-6.2.1.4610-linux/bin:$PATH
    ```

2. Provide the `SONAR_TOKEN`:

    - **Per Session (Temporary)**:
        ```bash
        export SONAR_TOKEN=<your_sonar_token>
        ```
    - **Global Setup (Persistent)**:  
      Edit the scanner properties file at:
        ```plaintext
        ~/.sonar/sonar-scanner-6.2.1.4610-linux/conf/sonar-scanner.properties
        ```
        Add this line:
        ```plaintext
        sonar.token=<your_sonar_token>
        ```

3. Generate a test Coverage report in XML format:

    ```bash
      	python -m pytest --cov=backend/src --cov-config=backend/setup.cfg --cov-report=xml:backend/coverage-reports/coverage.xml backend/src/tests/
        # or run make coverage
    ```

4. Run the scanner:
    ```bash
    sonar-scanner
    ```

**Tip:** Steps **3** & **4** can be streamlined with the make target `make sonar`

---

### **2. IDE Integration**

#### **VS Code**

1. Install the **SonarQube for IDE** extension from the VS Code Marketplace.
2. Add your SonarCloud account and project details in the extension settings.

#### **PyCharm**

1. Install the **SonarQube for IDE** plugin from the JetBrains Marketplace.
2. Configure the plugin:
    - Go to **File > Settings > Tools > SonarQube for IDE**.
    - Add your SonarCloud token and project details.

---

### **3. CI Configuration**

SonarScanner is integrated into the CI pipeline for automatic analysis. Key settings include:

- Coverage reports collected from the `test-backend` job.
- The `sonar-project.properties` file for project-specific configurations.

Refer to the [CI pipeline file](../.gitlab-ci.yml) for more details on the `sonarqube-scan` job.

---

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
