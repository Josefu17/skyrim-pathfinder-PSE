# CI/CD and Operation

This document outlines the CI/CD pipeline configuration and operations, including automated builds, tests, deployments,
and dependency management. It also touches on the topic of ensuring application availability.

---

## Table of Contents
1. [Pipeline to build the application](#pipeline-to-build-the-application)
2. [Trigger automated releases via GitLab](#trigger-automated-releases-via-gitlab)
3. [Deployment of application to a server](#deployment-of-application-to-a-server)
4. [Automated Tests](#automated-tests)
5. [Code Coverage and Displaying the Badge in GitLab](#code-coverage-and-displaying-the-badge-in-gitlab)
6. [Dependency proxy usage](#dependency-proxy-usage)
7. [Static Code Analysis (TODO)](#static-code-analysis)
8. [Ensuring application availability](#ensuring-application-availability)
9. [Scoped API tokens](#scoped-api-tokens)

---

## Pipeline to Build the Application

The pipeline builds and tests the application, ensuring it meets the required standards for deployment. This includes linting, formatting, unit tests, and code coverage analysis.

---

## Trigger Automated Releases via GitLab

Automated releases are triggered through the CI/CD pipeline using the `deploy` job. This ensures all tests and analyses
pass before the application is deployed. Secure access to the container registry and server is achieved using scoped API 
tokens and SSH keys.
---

## Deployment of Application to a Server

### Automated Deployment

Automated deployment is the primary method for deploying the application to the production server. It integrates Docker and SSH with GitLab CI/CD to build, push, and deploy Docker images.

1. **Building and Pushing Docker Images**:
   - The pipeline builds the Docker image using `make update` and pushes it to the registry:
     ```
     docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest .
     docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest
     ```

2. **Deployment on the Server**:
   - The `deploy` job runs remote commands via SSH using a secure API token to restart the application:
     ```bash
     ssh -i ci_ssh debian@group2 "cd ~/app && make update"
     ```
     The `make update` command performs the following:
     ```
     make login
     make stop
     make remove
     make start
     ```

---

### Manual Deployment (Fallback Method)

In case of pipeline failures or emergencies, manual deployment can be used. This involves running the deployment commands directly on the deployment server.

1. **Push the images:**
    - push the images to the deployment server from the local with:
   ```bash 
   make update
   ```

2. **Log into the Server**:
   ```bash
   ssh -i path/to/your/key debian@group2.devops-pse.users.h-da.cloud     
   ```

3. **Update the Container**:
   Navigate to the deployment directory and run:
   ```bash
   make update
   ```
   This command sequence performs the following:
   - Logs into the Docker registry.
   - Stops the current container.
   - Removes the old Docker image.
   - Pulls and starts the latest image.

---

## Automated Tests

The CI pipeline includes automated tests to ensure the application functions correctly before deployment. The tests cover:
- **Unit Tests**:
  - **Navigation Service**: [Unit Tests for Navigation Service](../backend/src/tests/unit)
  - **Backend**: [Unit Tests for Backend](../backend/src/tests/unit)
- **Code Coverage**: Verified as part of the pipeline, and a badge is displayed in the repository.
- **Startup Test for Separated Frontend**:
// TODO

### Test Job Configuration

Here’s a sample configuration for running tests in the pipeline:

```yaml
test-job:
  stage: test
  script:
    - pytest --cov=backend/src --cov-report=term backend/src/tests/ --cov-config=backend/setup.cfg
  coverage: '/TOTAL\s+\d+\s+\d+\s+(\d+)%/'
```

---

## Code Coverage and Displaying the Badge in GitLab

This part provides an overview of how to manage code coverage for the project, including running it locally, configuring the coverage tool, integrating it into the CI pipeline, and displaying a badge in GitLab.

### Steps to Display Code Coverage in GitLab

- **Local Coverage Check**: Run `pytest` with the coverage plugin:
  ```bash
  pytest --cov=backend/src --cov-report=term backend/src/tests/ 
  --cov-config=backend/setup.cfg
  ```
- **CI Integration**: Coverage is tested as part of the CI pipeline, the coverage is calculated with the help of a regex
from the terminal output.
- **Badge**: Add the markdown for the coverage badge from **GitLab Settings -> CI/CD -> General Pipelines** to the README file.


---

## Dependency Proxy Usage

The dependency proxy caches Docker images to reduce build times and ensure faster pipeline execution. The build job uses the proxy to pull the required base images.

```yaml
ci-build-job:
  stage: build
  image: ${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}/docker:latest
  services:
    - name: ${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}/docker:latest
      alias: docker
  script:
    - docker build -t "${CI_REGISTRY_IMAGE}:${CI_COMMIT_REF_SLUG}-${CI_COMMIT_SHA}" .
    - docker push "${CI_REGISTRY_IMAGE}:${CI_COMMIT_REF_SLUG}-${CI_COMMIT_SHA}"
```

## Static Code analysis

// TODO

---

## Ensuring Application Availability

### Monitoring Application Health

For an explanation for this, please refer to our `/healthz` endpoint implementation [here](API.md#health-check)

---

## Scoped API Tokens

Scoped API tokens are used for authentication in CI/CD processes, ensuring no personal credentials are stored on the 
server. Tokens can be created in GitLab under **Settings > Access Tokens** with the required scopes (`read_registry` 
and `write_registry`).

