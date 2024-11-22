# Project Management

## Issue Workflow Stages in GitLab

### Milestones
We’ve created Milestones to categorize our issues based on the core components and relevant aspects of our application:

- **Core Components:**
  - Web Frontend
  - Web Backend
  - Navigation Service
- **Other Relevant Aspects:**
  - DevExp
  - CI/CD and Operations

### Issue Workflow Stages
To manage the workflow of issues, we’ve defined the following stages:

1. **Backlog:**  
   - Represents our to-do list.  
   - Contains tasks we want to complete but haven’t started yet (unordered).  

2. **Doing:**  
   - Issues that are currently being worked on.  

3. **Review:**  
   - Issues waiting for a review from a colleague.  

4. **Done:**  
   - Issues that have been completed.  

### Developer Responsibilities
- Each developer is responsible for updating the status of their assigned issues.  
- GitLab’s built-in features, such as the `#closes <issue-id>` syntax, are partially used to automate updates.  


## Primary communication plattform

- Discord 

## Collaboration best practices

- Kanban
- Issue boards on [GitLab](https://code.fbi.h-da.de/bpse-wise2425/group2/-/boards)
- Meaningful names for variables and functions
- No direct commits on main branch
- Convention for commit messages
  - use imperative
  - **ADD**
  - **INIT**
  - **FIX**
  - **ADJUST**
  - **DELETE**
- Set priorities for issues
- New branches should use main as their starting point
- Improve issue descriptions by providing clear descriptions and any dependencies or prerequisites for 
an issue if applicable
- Ensure high code coverage and try to add tests to new components ASAP, ideally along the development!


### Merge Request Definition of Done

- Executable
- Tests(Unit / Integration)
- Fulfills requirements
- Code styling fulfilled
- Add documentation to changes

     

## Rules
- One [milestone](https://code.fbi.h-da.de/bpse-wise2425/group2/-/milestones) per stage 
- [Issue](https://code.fbi.h-da.de/bpse-wise2425/group2/-/issues) for each feature
- [Merge Request](https://code.fbi.h-da.de/bpse-wise2425/group2/-/merge_requests) for each feature addition
- Assign each merge request to at least one team member
- A merge request must be reviewed and approved by at least one other person before merging
- No direct commits to the main branch; it must remain clean.
