"""delete_task MCP tool for the AI Chatbot with MCP application."""

from sqlalchemy.orm import Session
from typing import Dict, Any
from ..models.user import User
from ..services.mcp_tool_service import MCPTool, MCPToolResult
from ..services.task_service import TaskService


class DeleteTaskTool(MCPTool):
    """MCP tool for deleting tasks."""
    
    def execute(self, **kwargs) -> MCPToolResult:
        """
        Execute the delete_task operation.
        
        Args:
            **kwargs: Must include 'task_id' of the task to delete
            
        Returns:
            MCPToolResult containing the result of the operation
        """
        try:
            # Validate required arguments
            if 'task_id' not in kwargs:
                return MCPToolResult(
                    success=False,
                    message="Missing required argument: 'task_id'",
                    error="Task ID is required to delete a task"
                )
            
            task_id = kwargs['task_id']
            
            # Delete task using TaskService
            task_service = TaskService(self.db_session)
            success = task_service.delete_task(self.user, task_id)
            
            if success:
                return MCPToolResult(
                    success=True,
                    message="Task has been deleted successfully",
                    data={
                        "task_id": task_id
                    }
                )
            else:
                return MCPToolResult(
                    success=False,
                    message="Task not found or you don't have permission to delete it",
                    error="Task not found or unauthorized"
                )
        
        except Exception as e:
            return MCPToolResult(
                success=False,
                message="Failed to delete task",
                error=str(e)
            )


# Register the tool with the MCP tool service
from ..services.mcp_tool_service import mcp_tool_service
mcp_tool_service.register_tool('delete_task', DeleteTaskTool)