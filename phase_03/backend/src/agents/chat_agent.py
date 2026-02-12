"""Chat agent for the AI Chatbot with MCP application."""

import json
from typing import Dict, Any, List, Optional
from openai import OpenAI
from src.config import settings
from src.services.mcp_tool_service import mcp_tool_service, MCPToolResult
from src.models.base_models import User
from sqlmodel import Session


class ChatAgent:
    """AI agent that interprets user intent and selects appropriate MCP tools."""
    
    def __init__(self, db: Session, user: User):
        """
        Initialize the chat agent.
        
        Args:
            db: Database session
            user: The authenticated user
        """
        self.db = db
        self.user = user
        self.client = OpenAI(api_key=settings.openai_api_key)
        
        # Define available tools for the agent
        self.available_tools = {
            "add_task": {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The task title"},
                            "description": {"type": "string", "description": "Optional task description"}
                        },
                        "required": ["title"]
                    }
                }
            },
            "list_tasks": {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List user's tasks, optionally filtered by status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "description": "Filter tasks by status (pending, in_progress, completed)"}
                        }
                    }
                }
            },
            "complete_task": {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The ID of the task to complete"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            "delete_task": {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The ID of the task to delete"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            "update_task": {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task's details",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "New title for the task"},
                            "description": {"type": "string", "description": "New description for the task"},
                            "status": {"type": "string", "description": "New status for the task (pending, in_progress, completed)"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        }
    
    def process_message(self, message: str, conversation_id: str) -> Dict[str, Any]:
        """
        Process a user message and return an appropriate response.
        
        Args:
            message: The user's message
            conversation_id: The ID of the conversation
            
        Returns:
            Dictionary containing the response and any tool calls made
        """
        # Call OpenAI API with function calling
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful task management assistant. Use the available functions to manage tasks. "
                                   "Always respond in a friendly, helpful way. If you can't understand the user's intent, "
                                   "ask for clarification."
                    },
                    {"role": "user", "content": message}
                ],
                tools=[self.available_tools[tool_name] for tool_name in self.available_tools],
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            tool_results = []
            assistant_response = ""
            
            if tool_calls:
                # Execute each tool call
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Execute the tool
                    result: MCPToolResult = mcp_tool_service.execute_tool(
                        function_name, 
                        self.db, 
                        self.user, 
                        **function_args
                    )
                    
                    tool_results.append({
                        "tool_name": function_name,
                        "arguments": function_args,
                        "result": {
                            "success": result.success,
                            "message": result.message,
                            "data": result.data,
                            "error": result.error
                        }
                    })
                
                # Generate final response based on tool results
                if response_message.content:
                    assistant_response = response_message.content
                else:
                    # If the model didn't provide content, create a summary based on tool results
                    success_count = sum(1 for tr in tool_results if tr["result"]["success"])
                    assistant_response = f"I've processed {success_count} of {len(tool_results)} requests successfully."
            else:
                # No tool calls were made, just return the model's response
                assistant_response = response_message.content or "I'm here to help you manage your tasks. What would you like to do?"
            
            return {
                "response": assistant_response,
                "tool_calls": tool_results,
                "conversation_id": conversation_id
            }
        
        except Exception as e:
            # Handle any errors gracefully
            return {
                "response": f"I'm sorry, I encountered an error processing your request: {str(e)}. Could you please try again?",
                "tool_calls": [],
                "conversation_id": conversation_id,
                "error": str(e)
            }
    
    def handle_ambiguous_intent(self, message: str) -> str:
        """
        Handle cases where the user's intent is ambiguous.
        
        Args:
            message: The user's ambiguous message
            
        Returns:
            A response asking for clarification
        """
        return "I'm not sure what you'd like me to do. Could you please clarify if you want to add, list, update, complete, or delete a task?"