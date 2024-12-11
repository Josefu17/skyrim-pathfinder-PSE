# Stage 1 Overview (Deadline 20.11.2024)

## Table of Contents
1. [Requirements of Stage 1](#stage-1-requirements)
2. [Retrospective Summary](#stage-1-retrospective-summary)

# **Stage 1 Requirements**

## Remaining Tasks:
### [Startup test for frontend](#cicd-and-operation)

## **Project Management**
- **[Merge Request Definition](../DoD.md#definition-of-done-dod)**  
  ✅ Completed  
- **[Set Issue Workflow](../Team-Practices.md#issue-workflow-stages)**  
  ✅ Completed  
- **[Primary Communication Platform](https://discord.com/)**  
  ✅ **Discord**  
- **[Collaboration Best Practices](../Team-Practices.md#collaboration-best-practices)**  
  ✅ Completed  

## **DevExp**
- **[Installation of Dependencies](../DevExp.md#one-click-installation)**  
  ✅ Completed  
- **[One-Click Start for Application](../DevExp.md#one-click-start-for-the-application-localdev)**  
  ✅ Completed  
- **[Tests Run Locally and in CI](../DevExp.md#tests-run-locally-and-in-ci)**  
  ✅ Completed  
- **[Linter and Formatter Setup](../DevExp.md#linter-and-formatter-setup)**  
  ✅ Completed  
- **[Debugger Setup](../DevExp.md#debugger-debugpy)**  
  ✅ Completed  
- **[Project's Setup Process + Major Design Decisions](../DevExp.md#projects-setup-process-and-major-design-decisions)**  
  ✅ Completed 

---

## **CI/CD and Operation**
- **[Pipeline to Build Application](../../.gitlab-ci.yml)**  
  ✅ Completed  
- **[Deployment of Application to Server](../ci-cd.md#deployment-of-application-to-a-server)**  
  ✅ Completed  
- **[Trigger Automated Releases via GitLab](../ci-cd.md#trigger-automated-releases-via-gitlab)**  
  ✅ Completed  
- **[Automated Tests](../ci-cd.md#automated-tests)**  
  - **[Unit Tests for Navigation Service](../../backend/src/tests/unit)** ✅ Completed  
  - **[Unit Tests for Backend](../../backend/src/tests/unit)** ✅ Completed  
  - **[Startup Test for Separated Frontend](../ci-cd.md#automated-tests)** ❌ Pending  
  - **[Display Code Coverage in GitLab](../ci-cd.md#code-coverage-and-displaying-the-badge-in-gitlab)** ✅ Completed  
- **[Linting and Formatting](../../README.md#linting-and-formatting)**  
  ✅ Completed  
- **[Dependency Proxy Usage](../ci-cd.md#dependency-proxy-usage)**  
  ✅ Completed  
- **[Code Analysis Tool(s)](../../README.md#code-analysis-with-sonarqube)**  
  ✅ Completed 
- **[Application Runs on Server](../ci-cd.md#ensuring-application-availability)**  
  ✅ Completed  
- **[Local Development with Local Database](../../README.md#running-the-application)** Our docker compose setup explained [here](../../README.md#running-the-application) allows this.  
  ✅ Completed  
- **[Database Migration Practices](../../README.md#migrations)**  
  - **No Database deletions, using migrations instead** ✅ Completed  
- **[Scoped API Tokens Instead of Real Credentials](../ci-cd.md#scoped-api-tokens)**  
  ✅ Completed  

---

## **Application**
- **[Stateless Navigation Service](../App.md#stateless-navigation-service)**  
  - **[Expose Route Calculation via RPC-API to Web Backend](../App.md#rpc-api)** ✅ Completed  
- **[Backend](../App.md#backend):**  
  - **[Fetch Map and Store in Database](../App.md#fetch-and-store-map)** ✅ Completed  
  - **[API Endpoints for Frontend](../API.md)** ✅ Completed  
- **[Frontend](../App.md#frontend)**  
  - **[Fetch and Display Map](../App.md#fetch-and-display-maps)** ✅ Completed  
  - **[Enable User Interaction](../App.md#user-interaction)** ✅ Completed  


# Stage 1 Retrospective Summary

## Key Takeaways

### Action Points
To improve our processes and address current challenges, the following action points were identified:

1. **Set Priorities for Issues**: Ensure issues are prioritized clearly to avoid wasting time on less critical tasks.

   ✅ Completed  
2. **Branches Must be Based on Main**: All new branches should always use the main branch as their starting point.

    ✅ Noted  
3. **Improve Issue Descriptions**: Issues without assigned owners must include a clear description of prerequisites to start work on them.

    ✅ Completed  
4. **Code Coverage for Current Code**: Create a high-priority branch focused on improving code coverage for existing code.

   ✅ Completed  
5. **Complete Stage 1**: Finish the pending tasks for Stage 1 as soon as possible.
    
    ❌ Pending 

To refer to our complete list of collaboration best practices, please refer to: 
[Collaboration Best Practices](../Team-Practices.md#collaboration-best-practices)

### Summary of Team Sentiments
- **Challenges Faced**: Recurring issues with the database setup and Python import errors led to frustration and wasted time.
- **Disappointments**: Some of the Stage 1 objectives were not fully achieved, including tests and an automated deployment setup.
- **Positives**: Team morale is high, with members enjoying the project overall and valuing the communication and teamwork. 
Quick review times and strong support from teammates were especially appreciated.

## Next Steps
The focus should be on tackling the action points above, particularly around prioritizing issues and increasing code 
coverage. Let’s aim to complete Stage 1 thoroughly and efficiently, while keeping our great team dynamic intact!
