"""complete_task MCP tool for the AI Chatbot with MCP application."""

from sqlalchemy.orm import Session
from typing import Dict, Any
from ..models.user import User
from ..services.mcp_tool_service import MCPTool, MCPToolResult
from ..services.task_service import TaskService


class CompleteTaskTool(MCPTool):
    """MCP tool for completing tasks."""
    
    def execute(self, **kwargs) -> MCPToolResult:
        """
        Execute the complete_task operation.
        
        Args:
            **kwargs: Must include 'task_id' of the task to complete
            
        Returns:
            MCPToolResult containing the result of the operation
        """
        try:
            # Validate required arguments
            if 'task_id' not in kwargs:
                return MCPToolResult(
                    success=False,
                    message="Missing required argument: 'task_id'",
                    error="Task ID is required to complete a task"
                )
            
            task_id = kwargs['task_id']
            
            # Complete task using TaskService
            task_service = TaskService(self.db_session)
            task = task_service.complete_task(self.user, task_id)
            
            if task:
                return MCPToolResult(
                    success=True,
                    message=f"Task '{task.title}' has been completed successfully",
                    data={
                        "task_id": str(task.id),
                        "title": task.title,
                        "status": task.status
                    }
                )
            else:
                return MCPToolResult(
                    success=False,
                    message="Task not found or you don't have permission to complete it",
                    error="Task not found or unauthorized"
                )
        
        except Exception as e:
            return MCPToolResult(
                success=False,
                message="Failed to complete task",
                error=str(e)
            )


# Register the tool with the MCP tool service
from ..services.mcp_tool_service import mcp_tool_service
mcp_tool_service.register_tool('complete_task', CompleteTaskTool)