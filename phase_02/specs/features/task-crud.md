# Feature: Task CRUD Operations
  
## User Stories 
- As a user, I can create a new task 
- As a user, I can view all my tasks 
- As a user, I can update a task 
- As a user, I can delete a task 
- As a user, I can mark a task complete 
- As a user, I am isolated from other users' tasks

## Acceptance Criteria 
### Create Task 
- Title is required (1-200 characters) 
- Description is optional (max 1000 characters) 
- Task is associated with logged-in user 

### View Tasks 
- Only show tasks for current user 
- Display title, status, created date 
- Support filtering by status 

### Update Task
- User can modify title and description
- Only the task owner can update the task

### Delete Task
- Only the task owner can delete the task

### Mark Complete
- Only the task owner can toggle completion status