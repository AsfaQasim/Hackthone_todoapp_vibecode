"""update_task MCP tool for the AI Chatbot with MCP application."""

from sqlalchemy.orm import Session
from typing import Dict, Any
from ..models.user import User
from ..services.mcp_tool_service import MCPTool, MCPToolResult
from ..services.task_service import TaskService


class UpdateTaskTool(MCPTool):
    """MCP tool for updating tasks."""
    
    def execute(self, **kwargs) -> MCPToolResult:
        """
        Execute the update_task operation.
        
        Args:
            **kwargs: Must include 'task_id' and at least one field to update
                    (title, description, status)
            
        Returns:
            MCPToolResult containing the result of the operation
        """
        try:
            # Validate required arguments
            if 'task_id' not in kwargs:
                return MCPToolResult(
                    success=False,
                    message="Missing required argument: 'task_id'",
                    error="Task ID is required to update a task"
                )
            
            task_id = kwargs['task_id']
            
            # Check if at least one update field is provided
            update_fields = {}
            if 'title' in kwargs:
                update_fields['title'] = kwargs['title']
            if 'description' in kwargs:
                update_fields['description'] = kwargs['description']
            if 'status' in kwargs:
                update_fields['status'] = kwargs['status']
            
            if not update_fields:
                return MCPToolResult(
                    success=False,
                    message="No fields to update provided",
                    error="At least one field (title, description, status) must be provided"
                )
            
            # Update task using TaskService
            task_service = TaskService(self.db_session)
            task = task_service.update_task(self.user, task_id, **update_fields)
            
            if task:
                return MCPToolResult(
                    success=True,
                    message=f"Task '{task.title}' has been updated successfully",
                    data={
                        "task_id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "status": task.status
                    }
                )
            else:
                return MCPToolResult(
                    success=False,
                    message="Task not found or you don't have permission to update it",
                    error="Task not found or unauthorized"
                )
        
        except Exception as e:
            return MCPToolResult(
                success=False,
                message="Failed to update task",
                error=str(e)
            )


# Register the tool with the MCP tool service
from ..services.mcp_tool_service import mcp_tool_service
mcp_tool_service.register_tool('update_task', UpdateTaskTool)