"""list_tasks MCP tool for the AI Chatbot with MCP application."""

from sqlalchemy.orm import Session
from typing import Dict, Any
from ..models.user import User
from ..services.mcp_tool_service import MCPTool, MCPToolResult
from ..services.task_service import TaskService


class ListTasksTool(MCPTool):
    """MCP tool for listing tasks."""
    
    def execute(self, **kwargs) -> MCPToolResult:
        """
        Execute the list_tasks operation.
        
        Args:
            **kwargs: Optional 'status' to filter tasks by status
            
        Returns:
            MCPToolResult containing the result of the operation
        """
        try:
            # Get optional status filter
            status_filter = kwargs.get('status', None)
            
            # Get tasks using TaskService
            task_service = TaskService(self.db_session)
            tasks = task_service.get_user_tasks(self.user, status_filter)
            
            # Format tasks for response
            tasks_data = []
            for task in tasks:
                tasks_data.append({
                    "task_id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None
                })
            
            status_msg = f" with status '{status_filter}'" if status_filter else ""
            return MCPToolResult(
                success=True,
                message=f"Found {len(tasks)} task(s){status_msg}",
                data={
                    "count": len(tasks),
                    "tasks": tasks_data
                }
            )
        
        except Exception as e:
            return MCPToolResult(
                success=False,
                message="Failed to list tasks",
                error=str(e)
            )


# Register the tool with the MCP tool service
from ..services.mcp_tool_service import mcp_tool_service
mcp_tool_service.register_tool('list_tasks', ListTasksTool)