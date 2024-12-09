# CI/CD and Operation

This document outlines the CI/CD pipeline configuration and operations, including automated builds, tests, deployments,
and dependency management. It also touches on the topic of ensuring application availability.

---

## Table of Contents

1. [Pipeline to Build the Application](#pipeline-to-build-the-application)  

2. [Trigger Automated Releases via GitLab](#trigger-automated-releases-via-gitlab)  
   - Using the `deploy` job for automated releases  

3. [Deployment of Application to a Server](#deployment-of-application-to-a-server)  
   - Automated deployment using Docker and SSH  
   - Manual deployment as a fallback  

4. [Automated Tests](#automated-tests)  
   - Unit tests and code coverage in the CI pipeline  

5. [Code Coverage and Displaying the Badge in GitLab](#code-coverage-and-displaying-the-badge-in-gitlab)  
   - Local checks, CI integration, and badge display setup  

6. [Dependency Proxy Usage](#dependency-proxy-usage)  
   - Using GitLab’s dependency proxy for faster pipelines  

7. [Ensuring Application Availability](#ensuring-application-availability)  
   - Health monitoring with `/healthz`  

8. [Scoped API Tokens](#scoped-api-tokens)  
   - Secure authentication for CI/CD processes  


## Pipeline to Build the Application

The pipeline builds and tests the application, ensuring it meets the required standards for deployment. 
This includes linting, formatting, unit tests, and code coverage analysis.

---

## Trigger Automated Releases via GitLab

Automated releases are triggered through the CI/CD pipeline using the `deploy` job. This ensures all tests and analyses
pass before the application is deployed. Secure access to the container registry and server is achieved using scoped API 
tokens and SSH keys.
---

## Deployment of Application to a Server

### Automated Deployment
The `deploy` job in the CI pipeline integrates Docker and SSH to deploy the application on the production server.

1. **Build and Push Docker Images**:  
   The pipeline builds the Docker image and pushes it to the registry:  
   ```bash
     docker build -t registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest .
     docker push registry.code.fbi.h-da.de/bpse-wise2425/group2/test-application:latest
   ```

2. **Deploy on Server**:  
   The `deploy` job runs remote commands via SSH:  
   ```bash
   ssh -i ci_ssh debian@group2 "cd ~/app && make update"
   ```  
   The `make update` command:  
   - Logs into the registry.  
   - Stops and removes the old container.  
   - Starts the latest image.

---

### Manual Deployment (Fallback)
In case of pipeline failures, manual deployment is a backup option.

1. **Push Images Locally**:
   ```bash
   make update
   ```

2. **Log into the Server**:
   ```bash
   ssh -i path/to/key debian@group2.server.com
   ```

3. **Deploy the Latest Image**:
   Navigate to the deployment directory and run:
   ```bash
   make update
   ```

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

---

## Ensuring Application Availability

### Monitoring Application Health

For an explanation for this, please refer to our `/healthz` endpoint implementation [here](API.md#health-check)

---

## Scoped API Tokens

Scoped API tokens are used for authentication in CI/CD processes, ensuring no personal credentials are stored on the 
server. Tokens can be created in GitLab under **Settings > Access Tokens** with the required scopes (`read_registry` 
and `write_registry`).
