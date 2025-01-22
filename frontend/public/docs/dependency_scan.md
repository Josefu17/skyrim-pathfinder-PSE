# GitLab Dependency Scanning with Scheduled Pipelines

## Overview

Dependency Scanning in GitLab automatically detects vulnerabilities in a project's dependencies. This was configured by including the pre-defined GitLab template for Dependency Scanning, which seamlessly integrates with the CI/CD pipeline.

Additionally, a **Scheduled Pipeline** was set up to run the Dependency Scanning job daily, ensuring regular checks for vulnerabilities without manual intervention.

## Configuration Summary

1. The `.gitlab-ci.yml` includes the following template:
    ```yaml
    include:
        - template: Security/Dependency-Scanning.gitlab-ci.yml
    ```
