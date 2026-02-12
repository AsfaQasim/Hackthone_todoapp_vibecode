# REST API Endpoints
  
## Base URL 
- Development: http://localhost:8000 
- Production: https://api.example.com 
  
## Authentication 
All endpoints require JWT token in header: 
Authorization: Bearer <token> 
  
## Endpoints 

### GET /api/tasks 
List all tasks for authenticated user. 
  
Query Parameters: 
- status: "all" | "pending" | "completed" 
- sort: "created" | "title" | "updated" 
  
Response: Array of Task objects 

### POST /api/tasks 
Create a new task. 
  
Request Body: 
- title: string (required, 1-200 chars) 
- description: string (optional, max 1000 chars) 
  
Response: Created Task object 

### GET /api/tasks/{id} 
Get a specific task by ID.
  
Response: Single Task object 

### PUT /api/tasks/{id} 
Update a specific task.
  
Request Body: 
- title: string (optional) 
- description: string (optional) 
- completed: boolean (optional) 
  
Response: Updated Task object 

### DELETE /api/tasks/{id} 
Delete a specific task.
  
Response: Empty response with 204 status 

### PATCH /api/tasks/{id}/complete 
Toggle completion status of a task.
  
Response: Updated Task object