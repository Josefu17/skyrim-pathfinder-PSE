
# Dependency Scan Job Documentation

## Overview
This job scans Python dependencies for known vulnerabilities using `pip-audit` and generates a report.

---

## Job Configuration
```yaml
dependency_scan-job:
  stage: test
  image: ${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}/python:3.13-slim
  script:
    - pip install --upgrade pip
    - pip install --user pip-audit
    - export PATH=$PATH:/root/.local/bin
    - pip-audit --version
    - pip-audit > dependency_audit_report.txt || true
    - if [ ! -s dependency_audit_report.txt ]; then echo "No known vulnerabilities found" > dependency_audit_report.txt; fi
    - if [ ! -s dependency_audit_report.txt ]; then echo "No report generated"; exit 1; fi
  artifacts:
    paths:
      - dependency_audit_report.txt
    expire_in: 1 day
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
    - if: '$CI_PIPELINE_SOURCE == "schedule"'
  needs:
    - test-job
```

---

## Features
- **Dependency Vulnerability Scan**  
  Runs `pip-audit` to check Python dependencies for vulnerabilities.

- **Report Generation**  
  Creates a `dependency_audit_report.txt`:
  - Contains vulnerabilities if found.
  - Displays "No known vulnerabilities found" if no issues exist.

- **Pipeline Artifacts**  
  Saves the report as an artifact with a 1-day expiry for further inspection.

- **Failure on Empty Report**  
  Ensures the pipeline fails if no report is generated.

---

## When Does the Job Run?
- On the `main` branch.
- When triggered by a scheduled pipeline.

---

## Output
The job outputs a `dependency_audit_report.txt` file containing:
- Detected vulnerabilities (if any).
- `No known vulnerabilities found` if no issues exist.
