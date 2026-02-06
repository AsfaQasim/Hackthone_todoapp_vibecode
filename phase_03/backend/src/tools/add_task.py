"""add_task MCP tool for the AI Chatbot with MCP application."""

from sqlalchemy.orm import Session
from typing import Dict, Any
from src.models.base_models import User
from ..services.mcp_tool_service import MCPTool, MCPToolResult
from ..services.task_service import TaskService


class AddTaskTool(MCPTool):
    """MCP tool for adding tasks."""
    
    def execute(self, **kwargs) -> MCPToolResult:
        """
        Execute the add_task operation.
        
        Args:
            **kwargs: Must include 'title' (and optionally 'description')
            
        Returns:
            MCPToolResult containing the result of the operation
        """
        try:
            # Validate required arguments
            if 'title' not in kwargs:
                return MCPToolResult(
                    success=False,
                    message="Missing required argument: 'title'",
                    error="Title is required to create a task"
                )
            
            title = kwargs['title']
            description = kwargs.get('description', None)
            
            # Create task using TaskService
            task_service = TaskService(self.db_session)
            task = task_service.create_task(self.user, title, description)
            
            return MCPToolResult(
                success=True,
                message=f"Task '{task.title}' has been added successfully",
                data={
                    "task_id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": task.status
                }
            )
        
        except Exception as e:
            return MCPToolResult(
                success=False,
                message="Failed to add task",
                error=str(e)
            )


# Register the tool with the MCP tool service
from ..services.mcp_tool_service import mcp_tool_service
mcp_tool_service.register_tool('add_task', AddTaskTool)