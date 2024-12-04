# Stage 2 Overview (Deadline 04.12.2024)

## Table of Contents
1. [Requirements of Stage 2](#requirements-of-stage-2)
2. [Retrospective Summary](#stage-2-retrospective-summary)
3. [Other Stages](#other-stages)

# Requirements of Stage 2

## Requirements from previous Stage
- Complete any missing requirements from Stage 1, as they are still relevant. For an overview, 
refer to: [Stage 1](stage_1.md)

## New Requirements
1. **Regularly update dependencies using the Renovate tool.**
2. **Implement a CI job for dependency vulnerability scanning:**
   - [x] Set up vulnerability scanning (e.g., GitLab dependency scanning).
   - [x] Schedule this check to run daily on the main branch and deployed version.
   - [x] Apply security patches promptly to keep the deployed application secure.

3. **Implement basic integration tests (optional, bonus points if implemented correctly):**
   - [ ] Automate a test that starts all services and performs at least one route calculation.(optional)
   - [x] Unit tests for the navigation service logic, with at least 90% code coverage.
   - [x] Unit tests for the Web Backend, ensuring the main flow is tested.
   - [x] Ensure the Frontend starts and verify that the main components are present.

4. **Ensure the application remains continuously running:**
   - [x] Provide a `/healthz` endpoint on the backend that returns the application's health status.
   - [x] Endpoint URL should be either:
     - `https://api.groupX.proxy.devops-pse.users.h-da.cloud/healthz`
     - `https://groupX.proxy.devops-pse.users.h-da.cloud/healthz`
   - [x] Response body should be JSON:
     ```json
     {
       "status": "healthy"
     }
     ```
     

---

# Stage 2 Retrospective Summary
// TBD

# Other Stages
- [Stage 1](stage_1.md)

[back to top](stage_2.md#table-of-contents)
