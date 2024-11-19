# CI/CD and Operation
Refer to the [CI/CD Operation Todo](./todo.md#cicd-and-operation) for an overview of related tasks and their current progress status. 
The following is a detailed explanation for them.
## Pipeline to build the application
## Deployment of application to a server
## Trigger automated releases via GitLab
## Automated tests
  ### unit tests for navigation service
  ### unit tests for backend
  ### startup test for seperated frontend
### Code Coverage and Displaying the Badge in GitLab
[back to top](#cicd-and-operation)
This part provides an overview of how to manage code coverage for the project, including running it locally, 
configuring the coverage tool, integrating it in the CI pipeline, and displaying a badge in GitLab.

#### 1. Running Coverage Check Locally

To check code coverage locally, we use `pytest` along with the `coverage` plugin. Follow these steps to run the coverage check:

1. Running the coverage command:

   ```sh
   pytest --cov=src --cov-report=html src/tests/ --cov-config=setup.cfg
   ```

   This command will create a detailed HTML report of the code coverage. To open the HTML report automatically, you can add:

   ```sh
   open htmlcov/index.html  # For macOS
   xdg-open htmlcov/index.html  # For Linux
   start htmlcov\index.html  # For Windows
   ```
   The combined command would then look like this (e.g. for Windows):
    ```sh
   pytest --cov=src --cov-report=html src/tests/ --cov-config=setup.cfg && start htmlcov\index.html
   ```

2. A `.coverage` file is generated automatically for the calculation of the coverage, this can safely be deleted later on,
alternatively it could be added to gitignore to one's desire. 

#### 2. Configuration File (setup.cfg)

We use `setup.cfg` to configure the behavior of the coverage tool. Below is an example of the relevant section of `setup.cfg`:

```ini
[coverage:run]
omit =
    src/tests/*

[coverage:report]
show_missing = True
```
- **`omit`**: This section specifies files or directories to exclude from the coverage report. The tool considers only
python files by default, so explicitly excluding other file types isn't necessary.
- **`show_missing`**: Shows lines of code that are not covered by tests in the terminal report.

#### 3. Running Coverage in CI
The GitLab CI pipeline is configured to run tests and generate a coverage report. Below is an excerpt of the relevant 
part of .gitlab-ci.yml:

```yaml
stages:
  - test
test-job:
  stage: test
  script:
    -     - pytest --cov=src -cov-report=xml:coverage.xml src/tests/ --cov-config=setup.cfg
  artifacts:
    paths:
      - coverage.xml
```

- **Artifacts**: The `coverage.xml` file is stored as an artifact and used for further analysis, including generating 
a coverage badge.

#### 4. Displaying the Code Coverage Badge in GitLab

To display a code coverage badge in GitLab:

- GitLab automatically creates coverage badges for each branch. The necessary markdown snippet for the badge can be found
under:
  - **settings -> CI/CD -> General Pipelines**
- To display the badge, simply add the markdown to your README file.

#### 5. Summary
- **Local Coverage Check**: Run `pytest` with the coverage plugin to generate HTML reports.
- **Configuration**: Use `setup.cfg` to manage which files to include or omit from the coverage.
- **CI Integration**: Coverage is tested as part of the CI pipeline, storing `coverage.xml` as an artifact.
- **Badge**: Display a coverage badge in the GitLab repository to track overall test coverage.


## Linting and formatting
We use Pylint as the linter and Black as the formatter. In the CI pipeline, we install the libraries and apply them to every Python file in the `src` folder. The analyze-job fails if the code does not achieve a 10/10 rating.
```
before_script:
  - pip install -r requirements.txt
script:
  - python -m pylint src/*.py
  - python -m black src/*.py
```
## dependency proxy usage 
## code analysis tools 
## application runs on server
## local development with a local database
The Postgres image is running locally in the following Docker container:
```
postgres:
  image: postgres:latest
  environment:
    POSTGRES_USER: pg-2
    POSTGRES_PASSWORD: pg-2
    POSTGRES_DB: navigation
  ports:
    - "5433:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
  networks:
    - app-network
```
## The production database must never be deleted; only apply migrations **???**
## No real credentials (e.g. for log in to the container registry) should be on the server, only scoped API tokens

An access token is created on GitLab via **Settings &rightarrow; Access Tokens**. The token must have at least the **Developer** role and the **read_registry** scope.

It is used to log into the Docker registry of the server.
```
docker login registry.code.fbi.h-da.de
```
