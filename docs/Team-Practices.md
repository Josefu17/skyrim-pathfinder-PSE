# Development and Collaboration Guidelines

This document provides guidelines for development and collaboration, including code styling conventions, project 
management workflows, and issue naming standards. It aims to support efficient task tracking, clear communication, and 
consistent code quality.

---

## Table of Contents
1. [Tech Stack and Styling Conventions](#tech-stack-and-code-styling)
2. [Project Management](#project-management)
3. [Issue Naming and Classification Convention](#issue-naming-and-classification)
4. [Collaboration Best Practices](#collaboration-best-practices)
5. [Rules](#rules)

## Tech Stack and Code Styling

### Designated Languages
- **Backend**: Python (Flask-based REST API)
- **Navigation Service**: Python (XML-RPC service for route calculations)
- **Database**: PostgreSQL
- **Frontend**: HTML/JavaScript/CSS

### Styling Conventions
- Use **snake_case** for variables, functions, and file names (e.g., `example_name`).
- All code and comments must be in **English**.
- Indentation: Use **4 spaces** for Python.
- **Linter**: `pylint`
- **Formatter**: `black`

## Project Management

### Issue Workflow Stages

#### Milestones
Milestones categorize issues into key application components:
- **Web Frontend**
- **Web Backend**
- **Navigation Service**
- **DevExp**
- **CI/CD and Operations**

#### Workflow Stages
1. **Backlog**: Tasks not started yet.
2. **Doing**: Tasks in progress.
3. **Review**: Tasks awaiting review.
4. **Done**: Completed tasks.

### Developer Responsibilities
- Update issue statuses promptly.
- Use GitLab features like `#Closes <issue-id>` to automate updates.
- Adhere to naming conventions and meaningful commit messages:
  - Examples: `ADD`, `FIX`, `DELETE`, `ADJUST`, `INIT`

[Back to Top](#development-and-collaboration-guidelines)

---

## **Issue Naming and Classification**

### **Task Domains**
Classify issues based on their type of work:
- **Bug**: Errors in code or functionality causing unexpected behavior.
- **Feature**: New functionalities or extensions to be added to the system.
- **Enhancement**: Improvements or optimizations to existing features.
- **Task**: General tasks that support the development process but do not directly impact functionality.
- **Test**: Creating or executing tests for features or bug fixes.
- **Documentation**: Creating or updating project documentation.

### **Project Domains**
Categorize issues by the relevant project area:
- **Backend**
- **Navigation**
- **Frontend**

### **Issue Naming Convention**
Follow this naming format for issues:
`[Project-DOMAIN]TASK-DOMAIN: Description of the issue`

#### **Examples**
- `[Backend]Bug: Fix login timeout error`
- `[Frontend]Feature: Add search bar to the UI`
- `[Navigation]Enhancement: Optimize route calculation algorithm`

---

## Collaboration Best Practices

### Tools
- Primary communication: **Discord**
- Task tracking: [GitLab Issue Boards](https://code.fbi.h-da.de/bpse-wise2425/group2/-/boards)

### Practices
- Use **Kanban** methodology for issue tracking.
- Create branches from `main` and avoid direct commits to it.
- Prioritize high coverage for tests alongside development.
- Write clear issue descriptions with prerequisites when necessary.

### Merge Request Definition of Done

- Kindly refer to [Definition of Done Documentation](DoD.md#definition-of-done-dod) for this.

---

## Rules

1. **Milestones**: One milestone per stage.
2. **Issues**: One issue per feature.
3. **Merge Requests**: All new features require an MR reviewed by another developer.
4. **Main Branch**: Remains clean and deployment-ready; no direct commits.

[Back to Top](#development-and-collaboration-guidelines)
