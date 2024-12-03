# Stage 1 Overview (Deadline 20.11.2024)

## Table of Contents
- [Requirements of Stage 1](#requirements-of-stage-1)
- [Retrospective Summary](#stage-1-retrospective-summary)

# Requirements of Stage 1

## Project Management

- [x] Merge request Definition [**Documentation**](../management.md#Merge-Request-Definition-of-Done)
- [x] Set issue workflow [**Documentation**](../management.md#Issue-Workflow-Stages-in-GitLab)
- [x] Primary communication plattform: **Discord**
- [x] Collaboration best practises + [**Documentation**](../management.md#collaboration-best-practices)

## DevExp

- [x] Installation of dependencies with a "one-click" + [**Documentation**](../devexp.md#one-click-installation)
- [x] Start the application with "one-click" + [**Documentation**](../devexp.md#one-click-start-for-the-application-localdev)
- [x] Tests that run locally and in CI + [**Documentation**](../devexp.md#tests-run-locally-and-in-ci)
- [x] Linter/formatter local and in CI + [**Documentation**](../devexp.md#linter-and-formatter-setup)
- [x] Debugger + [**Documentation**](../devexp.md#debugger-debugpy) 
- [ ] Project's setup process + Major design decision + [**Documentation**](../devexp.md#projects-setup-process-and-major-design-decisions)

## CI/CD and Operation

- [x] Pipeline to build the application
- [x] Deployment of application to a server + [**Documentation**](../ci.md#deployment-of-application-to-a-server)
- [x] Trigger automated releases via GitLab + [**Documentation**](../ci.md#trigger-automated-releases-via-gitlab)
- [ ] Automated tests
  - [x] unit tests for navigation service
  - [x] unit tests for backend
  - [ ] startup test for seperated frontend
  - [x] Display code coverage in GitLab with an icon + [**Documentation**](../ci.md#code-coverage-and-displaying-the-badge-in-gitlab)
- [x] Linting and formatting
- [x] dependency proxy usage 
- [ ] code analysis tools 
- [x] application runs on server
- [x] local development with a local database
- [x] The production database must never be deleted; only apply migrations
- [x] No real credentials (e.g. for log in to the container registry) should be on the server, only scoped API
tokens

## Application
- [x] [Stateless navigation service](../app.md#stateless-navigation-service)
  - [x] Expose the route calculation functionality via an [RPC-API](../app.md#rpc-api) to the Web Backend
- [x] Backend
  - [x] Fetch map and store it in database
  - [x] API endpoints for the frontend
- [x] Frontend
  - [x] Fetch and display map
  - [x] User interaction


# Stage 1 Retrospective Summary

## Key Takeaways

### Action Points
To improve our processes and address current challenges, the following action points were identified:

1. **Set Priorities for Issues**: Ensure issues are prioritized clearly to avoid wasting time on less critical tasks.
2. **Branches Must be Based on Main**: All new branches should always use the main branch as their starting point.
3. **Improve Issue Descriptions**: Issues without assigned owners must include a clear description of prerequisites to start work on them.
4. **Code Coverage for Current Code**: Create a high-priority branch focused on improving code coverage for existing code.
5. **Complete Stage 1**: Finish the pending tasks for Stage 1 as soon as possible.

To refer to our complete list of collaboration best practices, please refer to: 
[Collaboration Best Practices](../management.md#collaboration-best-practices)

### Summary of Team Sentiments
- **Challenges Faced**: Recurring issues with the database setup and Python import errors led to frustration and wasted time.
- **Disappointments**: Some of the Stage 1 objectives were not fully achieved, including tests and an automated deployment setup.
- **Positives**: Team morale is high, with members enjoying the project overall and valuing the communication and teamwork. 
Quick review times and strong support from teammates were especially appreciated.

## Next Steps
The focus should be on tackling the action points above, particularly around prioritizing issues and increasing code 
coverage. Let’s aim to complete Stage 1 thoroughly and efficiently, while keeping our great team dynamic intact!


