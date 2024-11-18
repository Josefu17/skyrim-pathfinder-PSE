# CI/CD and Operation
## Pipeline to build the application
## Deployment of application to a server
## Trigger automated releases via GitLab
## Automated tests
  ### unit tests for navigation service
  ### unit tests for backend
  ### startup test for seperated frontend
  ### Display code coverage in GitLab with an icon 
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
