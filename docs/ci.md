# CI/CD and Operation

Refer to the [CI/CD Operation Todo](Stages/stage_1.md#cicd-and-operation) for an overview of related tasks and their
current progress status.
The following is a detailed explanation for them.

## Table of Contents
1. [Pipeline to build the application](#pipeline-to-build-the-application)
2. [Deployment of application to a server](#deployment-of-application-to-a-server)
3. [Trigger automated releases via GitLab](#trigger-automated-releases-via-gitlab)
4. [Linting and formatting](#linting-and-formatting)
5. [dependency proxy usage](#dependency-proxy-usage)
6. [code analysis tools](#code-analysis-tools)
7. [making sure application runs on server](#making-sure-application-runs-on-server)
8. [Scoped API tokens](#scoped-api-tokens)

## Pipeline to build the application

## Deployment of application to a server

The application runs successfully on the production server, with all changes deployed seamlessly from the local
environment. Executing make update in the git root directory builds and pushes the Docker image to the container
registry. On the deployment server, running make update updates and restarts the container, completing the deployment
process. For detailed steps,
see [Update Docker Container (from local to server)](Docker.md#update-docker-container-from-local-to-server).

## Trigger automated releases via GitLab

The `deploy` job automates the secure deployment of the application to a production server. It ensures that all required
tests and analyses are successfully completed before updating the application.

By leveragingDocker-in-Docker (DinD), the deployment process performs a Docker login using `make login` and builds and
pushes the images to `registry.code.fbi.h-da.de/bpse-wise2425/group2` using `make update`, all within the
`establish_ssh_connection.sh` script. GitLab Secure Files and API tokens are utilized to access the container registry,
eliminating the need for real credentials.

After the images are prepared, remote commands are executed on the production
server using SSH. The script connects securely to the server via the `ci_ssh` key and runs the `make update` command,
ensuring the application is deployed and confirmed with a success message. This setup combines Docker and SSH to enable
efficient, automated, and reliable deployments.

### Automated Tests

The CI pipeline includes automated tests to ensure the application functions correctly before deployment. The tests cover:
- **Unit Tests**: Validate individual components like the navigation service and backend.
- **Code Coverage**: Verified as part of the pipeline, and a badge is displayed in the repository.

Here’s a sample configuration for running tests in the pipeline:

```yaml
test-job:
  stage: test
  script:
    - pytest --cov=backend/src --cov-report=term backend/src/tests/ --cov-config=backend/setup.cfg
  coverage: '/TOTAL\s+\d+\s+\d+\s+(\d+)%/'

```

For detailed test implementations, refer to the corresponding service test files:
- **Navigation Service**: [Navigation Service Tests](../backend/src/tests)
- **Backend**: [Backend Tests](../backend/src/tests)


### startup test for seperated frontend
// TODO

[back to top](#cicd-and-operation)

### Code Coverage and Displaying the Badge in GitLab

This part provides an overview of how to manage code coverage for the project, including running it locally,
configuring the coverage tool, integrating it in the CI pipeline, and displaying a badge in GitLab.

#### 1. Running Coverage Check Locally

To check code coverage locally, we use `pytest` along with the `coverage` plugin. Follow these steps to run the coverage
check:

1. Running the coverage command:

   ```sh
   pytest --cov=src --cov-report=html src/tests/ --cov-config=setup.cfg
   ```

   This command will create a detailed HTML report of the code coverage. To open the HTML report automatically, you can
   add:

   ```sh
   open htmlcov/index.html  # For macOS
   xdg-open htmlcov/index.html  # For Linux
   start htmlcov\index.html  # For Windows
   ```
   The combined command would then look like this (e.g. for Windows):
    ```sh
   pytest --cov=src --cov-report=html src/tests/ --cov-config=setup.cfg && start htmlcov\index.html
   ```

2. A `.coverage` file is generated automatically for the calculation of the coverage, this can safely be deleted later
   on,
   alternatively it could be added to gitignore to one's desire.

#### 2. Configuration File (setup.cfg)

We use `setup.cfg` to configure the behavior of the coverage tool. Below is an example of the relevant section of
`setup.cfg`:

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
    - - pytest --cov=src -cov-report=xml:coverage.xml src/tests/ --cov-config=setup.cfg
  artifacts:
    paths:
      - coverage.xml
```

- **Artifacts**: The `coverage.xml` file is stored as an artifact and used for further analysis, including generating
  a coverage badge.

#### 4. Displaying the Code Coverage Badge in GitLab

To display a code coverage badge in GitLab:

- GitLab automatically creates coverage badges for each branch. The necessary markdown snippet for the badge can be
  found
  under:
    - **settings -> CI/CD -> General Pipelines**
- To display the badge, simply add the markdown to your README file.

#### 5. Summary

- **Local Coverage Check**: Run `pytest` with the coverage plugin to generate HTML reports.
- **Configuration**: Use `setup.cfg` to manage which files to include or omit from the coverage.
- **CI Integration**: Coverage is tested as part of the CI pipeline, storing `coverage.xml` as an artifact.
- **Badge**: Display a coverage badge in the GitLab repository to track overall test coverage.

[back to top](#cicd-and-operation)
## Linting and formatting

We use Pylint as the linter and Black as the formatter. In the CI pipeline, we install the libraries and apply them to
every Python file in the `src` folder. The analyze-job fails if the code does not achieve a 10/10 rating.

```
before_script:
  - pip install -r backend/requirements.txt
script:
  - python -m pylint --rcfile=backend/.pylintrc backend/src
  - python -m black --config backend/pyproject.toml backend/src
```

## dependency proxy usage

We use the provided dependency proxy to use cache the images in the proxy so that they aren't pulled anew everytime
we run our pipeline. Here is a snippet from our gitlab-ci.yml file. The build job builds an image for other jobs in the
pipeline to use.

```yaml
ci-build-job:
  stage: build
  image: ${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}/docker:latest
  services:
    - name: ${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}/docker:latest
      alias: docker
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t "${CI_REGISTRY_IMAGE}:${CI_COMMIT_REF_SLUG}-${CI_COMMIT_SHA}" --build-arg "GITLAB_PROXY=${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}/" .
    - docker push "${CI_REGISTRY_IMAGE}:${CI_COMMIT_REF_SLUG}-${CI_COMMIT_SHA}"


test-job:
  stage: test
  image: ${CI_REGISTRY_IMAGE}:${CI_COMMIT_REF_SLUG}-${CI_COMMIT_SHA}
```

## code analysis tools
// TODO

[back to top](#cicd-and-operation)
## making sure application runs on server

### Monitoring Application Health

To confirm the application remains operational, the following steps are recommended:

1. **Automated Monitoring**:
   In real-world systems, automated monitoring tools like **Pingdom** (for external uptime checks) or **Prometheus with Alertmanager** (for internal health monitoring) would be used to periodically check the `/healthz` endpoint and send alerts in case of failures.

   As a simplified alternative, we provide an example of setting up a cronjob on the production server to periodically check the `/healthz` endpoint and send an email if the health check fails. Below is the example script:

   ```bash
   #!/bin/bash

   # URL of the health check endpoint
   HEALTH_URL="https://localhost:4243/healthz"

   # Email to notify in case of failure
   NOTIFY_EMAIL="test@example.com"

   # Run the health check
   RESPONSE=$(curl -s -w "\n%{http_code}" "$HEALTH_URL")
   BODY=$(echo "$RESPONSE" | head -n -1)
   STATUS=$(echo "$RESPONSE" | tail -n 1)

   # Write body to a temporary file for grep
   echo "$BODY" > /tmp/health_check_response.json

   # Check HTTP status and health response
   if [[ "$STATUS" != "200" ]] || ! echo "$BODY" | grep -q '"status": "healthy"'; then
       echo "Health check failed for $HEALTH_URL at $(date)" | mail -s "!!! SOUND THE BELLS, PROD IS DOWN !!!" "$NOTIFY_EMAIL"
   else
       echo "Health check passed for $HEALTH_URL at $(date)"
   fi

   echo "Script ran at $(date)"
   ```

   #### Scheduling the Script:
   - Use a cronjob to schedule this script. For example, to run it daily:
     ```bash
     0 0 * * * /path/to/healthz-check-cronjob.sh >> /var/log/healthz-check.log 2>&1
     ```

   #### Notes:
   - The script is designed for use within the deployment server environment, where the `/healthz` endpoint is accessible locally.
   - **This script is not currently set up in our project** but is included for demonstration purposes, showcasing a lightweight approach to monitoring service health.

## Scoped API tokens

**No real credentials (e.g. for log in to the container registry) should be on the server, only scoped API tokens are used**

An access token is created on GitLab via **Settings &rightarrow; Access Tokens**. The token must have at least the *
*Developer** role and the **read_registry** scope.

It is used to log into the Docker registry of the server.

```
docker login registry.code.fbi.h-da.de
```

[back to top](#cicd-and-operation)
