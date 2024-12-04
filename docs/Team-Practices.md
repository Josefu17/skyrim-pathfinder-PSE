# Development and Collaboration Guidelines

## Table of Contents
1. [Code Styling](#code-styling)
2. [Project Management](#project-management)
3. [Collaboration Best Practices](#collaboration-best-practices)
4. [Rules](#rules)

## Code Styling

### Designated Languages
- **Backend**: Python
- **Navigation Service**: XML-RPC
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
- Use GitLab features like `#closes <issue-id>` to automate updates.
- Adhere to naming conventions and meaningful commit messages:
  - Examples: `ADD`, `FIX`, `DELETE`, `ADJUST`, `INIT`

[Back to Top](#development-and-collaboration-guidelines)
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
