"""MCP tool framework ensuring tools receive all data via parameters."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.models.base_models import User


class MCPToolResult(BaseModel):
    """Result from an MCP tool execution."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class MCPTool(ABC):
    """Abstract base class for MCP tools."""
    
    def __init__(self, db_session: Session, user: User):
        """
        Initialize the MCP tool with database session and user context.
        
        Args:
            db_session: Database session for the operation
            user: User object representing the authenticated user
        """
        self.db_session = db_session
        self.user = user
    
    @abstractmethod
    def execute(self, **kwargs) -> MCPToolResult:
        """
        Execute the MCP tool with the provided arguments.
        
        Args:
            **kwargs: Tool-specific arguments
            
        Returns:
            MCPToolResult containing the result of the operation
        """
        pass
    
    def validate_user_ownership(self, resource_user_id: str) -> bool:
        """
        Validate that the resource belongs to the authenticated user.
        
        Args:
            resource_user_id: ID of the user who owns the resource
            
        Returns:
            True if the user owns the resource, False otherwise
        """
        return str(self.user.id) == str(resource_user_id)


class MCPToolService:
    """Service to manage and execute MCP tools."""
    
    def __init__(self):
        self.tools = {}
    
    def register_tool(self, name: str, tool_class: type):
        """Register an MCP tool with the service."""
        self.tools[name] = tool_class
    
    def get_tool(self, name: str) -> type:
        """Get a registered MCP tool by name."""
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' is not registered")
        return self.tools[name]
    
    def execute_tool(self, name: str, db_session: Session, user: User, **kwargs) -> MCPToolResult:
        """Execute a registered MCP tool."""
        tool_class = self.get_tool(name)
        tool_instance = tool_class(db_session, user)
        return tool_instance.execute(**kwargs)


# Global MCP tool service instance
mcp_tool_service = MCPToolService()