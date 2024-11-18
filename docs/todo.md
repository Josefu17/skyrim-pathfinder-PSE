# Todos for Stage 1


## Project Management

- [x] Merge request Definition 
- [x] Set issue workflow
- [x] Primary communication plattform
- [x] Collaboration best practises + [**Documentation**](management.md#collaboration-best-practices)

## DevExp

- [x] Installation of dependencies with a "one-click" + [**Documentation**](devexp.md#one-click-installation)
- [x] Start the application with "one-click" + [**Documentation**](devexp.md#one-click-start-for-the-application-localdev)
- [x] Tests that run locally and in CI + [**Documentation**](devexp.md#tests-run-locally-and-in-ci)
- [x] Linter/formatter local and in CI + [**Documentation**](devexp.md#linter-and-formatter-setup)
- [ ] Debugger + [**Documentation**](devexp.md#debugger-debugpy) 
- [ ] Project's setup process + Major design decision + [**Documentation**](devexp.md#projects-setup-process-and-major-design-decisions)

## CI/CD and Operation

- [ ] Pipeline to build the application
- [ ] Deployment of application to a server
- [ ] Trigger automated releases via GitLab
- [ ] Automated tests
  - [x] unit tests for navigation service
  - [ ] unit tests for backend
  - [ ] startup test for seperated frontend
  - [ ] Display code coverage in GitLab with an icon 
- [x] Linting and formatting
- [x] dependency proxy usage 
- [ ] code analysis tools 
- [ ] application runs on server
- [x] local development with a local database
- [ ] The production database must never be deleted; only apply migrations **???**
- [x] No real credentials (e.g. for log in to the container registry) should be on the server, only scoped API
tokens

## Application
- [x] [Stateless navigation service](app.md#stateless-navigation-service)
  - [x] Expose the route calculation functionality via an [RPC-API](app.md#rpc-api) to the Web Backend
- [x] Backend
  - [x] Fetch map and store it in database
  - [x] API endpoints for the frontend
- [ ] Frontend
  - [ ] Fetch and display map
  - [ ] User interaction
