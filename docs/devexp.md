# DevExp
Refer to the [DevExp Todo](Stages/stage_1.md#devexp) for an overview of related tasks and their current progress status. 
The following is a detailed explanation for them.
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

```
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

#### Setup for pycharm
// TODO

## One-Click installation
[back to top](#DevExp)
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

## One-Click Start for the Application (localdev)
[back to top](#DevExp)

### Overview
The application can be started locally with a single command using the `Makefile`. This command initializes all services (Postgres, Navigation Service, Web Backend) defined in the `docker-compose.yml` file.

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



## Tests run locally and in CI
[back to top](#DevExp)

With ``pytest``, we have created tests for our features that can be run locally. In the CI, they run in the 'test-job'. Python files starting with 'test' are executed with ``python -m pytest``.

```
script:
    - python -m pytest ./src/test*.py --verbose
```

## Linter and Formatter Setup
[back to top](#DevExp)

### Overview
We use:
- **Linter**: `pylint` (configuration in `.pylintrc`)
- **Formatter**: `black` (configuration in `pyproject.toml`)

Both tools are configured to run locally and in the CI pipeline with the same settings to ensure consistent code quality.

---

### Local Setup

1. **Install Dependencies**:
   Use the `Makefile`:
   ```bash
   make install
   ```

2. **Run Linter and Formatter**:
   ```bash
   python -m pylint --rcfile=.pylintrc src/*.py
   python -m black --config pyproject.toml src/*.py
   ```

3. **Run Inside Docker**:
   ```bash
   docker exec -it <container-name> sh -c "
      python -m pylint --rcfile=.pylintrc src/*.py &&
      python -m black --config pyproject.toml src/*.py
   "
   ```

---

### CI Pipeline

1. **Install Dependencies**:
   The `analyze-job` in the CI pipeline installs the tools:
   ```yaml
   before_script:
     - pip install -r requirements.txt
   ```

2. **Run Linter and Formatter**:
   The CI pipeline validates code with:
   ```yaml
   script:
     - python -m pylint --rcfile=.pylintrc src/*.py
     - python -m black --config pyproject.toml src/*.py
   ```

---

### Ensuring Consistency
- **Single Source of Truth**: The `.pylintrc` and `pyproject.toml` files ensure consistent rules across all environments.
  - A note on this: Our configuration files are either pretty much the same as the default or contain minimal differences / configurations,
  we still decided to generate and specify the configuration files explicitly to enforce consistency between local 
  development and CI Pipeline.
- **Pre-commit Hooks** (Optional): Use `pre-commit` to automate checks locally before committing code.

## Project's setup process and major design decisions
[back to top](#DevExp)
// TODO
