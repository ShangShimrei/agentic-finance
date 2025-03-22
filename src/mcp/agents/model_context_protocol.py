"""
Model Context Protocol (MCP) module that manages context and coordinates tool calls across agents.
"""
import logging
from typing import Dict, Any, List, Optional, Callable
import inspect
import json

logger = logging.getLogger(__name__)

class ModelContextProtocol:
    """
    Model Context Protocol (MCP) manages context and coordinates tool calls across trading agents.
    Acts as a central coordination layer that maintains context across the system.
    """
    
    def __init__(self):
        """Initialize the Model Context Protocol."""
        self.context = {}
        self.tools = {}
        self.registered_agents = {}
        self.history = []
        logger.info("Initializing Model Context Protocol")
    
    def register_agent(self, agent_name: str, agent_instance: Any) -> None:
        """
        Register an agent with the MCP.
        
        Args:
            agent_name: Name of the agent
            agent_instance: Instance of the agent
        """
        self.registered_agents[agent_name] = agent_instance
        logger.info(f"Registered agent: {agent_name}")
    
    def register_tool(self, tool_name: str, tool_func: Callable, description: str) -> None:
        """
        Register a tool function that can be called by agents.
        
        Args:
            tool_name: Name of the tool
            tool_func: Function to execute
            description: Description of the tool
        """
        self.tools[tool_name] = {
            "function": tool_func,
            "description": description,
            "signature": inspect.signature(tool_func)
        }
        logger.info(f"Registered tool: {tool_name}")
    
    def update_context(self, key: str, value: Any) -> None:
        """
        Update the shared context with new information.
        
        Args:
            key: Context key
            value: Context value
        """
        self.context[key] = value
        logger.debug(f"Updated context: {key}")
    
    def get_context(self, key: str = None) -> Any:
        """
        Get information from the shared context.
        
        Args:
            key: Context key to retrieve (None returns entire context)
            
        Returns:
            Context value or entire context
        """
        if key is None:
            return self.context
        
        return self.context.get(key)
    
    def call_tool(self, tool_name: str, agent_name: str, **kwargs) -> Any:
        """
        Execute a tool on behalf of an agent.
        
        Args:
            tool_name: Name of the tool to call
            agent_name: Name of the agent making the call
            **kwargs: Arguments to pass to the tool
            
        Returns:
            Tool execution result
        """
        if tool_name not in self.tools:
            logger.error(f"Tool not found: {tool_name}")
            return {"error": f"Tool {tool_name} not found"}
        
        tool = self.tools[tool_name]
        
        # Log the tool call
        logger.info(f"Agent {agent_name} calling tool {tool_name}")
        
        try:
            # Execute the tool
            result = tool["function"](**kwargs)
            
            # Record the call in history
            self.history.append({
                "timestamp": logging.Formatter.converter(),
                "agent": agent_name,
                "tool": tool_name,
                "arguments": kwargs,
                "status": "success"
            })
            
            return result
        
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            
            # Record the failed call
            self.history.append({
                "timestamp": logging.Formatter.converter(),
                "agent": agent_name,
                "tool": tool_name,
                "arguments": kwargs,
                "status": "error",
                "error": str(e)
            })
            
            return {"error": str(e)}
    
    def get_tool_description(self, tool_name: str = None) -> Dict[str, Any]:
        """
        Get descriptions of available tools.
        
        Args:
            tool_name: Specific tool to get information for (None returns all)
            
        Returns:
            Tool descriptions
        """
        if tool_name is not None:
            if tool_name in self.tools:
                tool = self.tools[tool_name]
                return {
                    "name": tool_name,
                    "description": tool["description"],
                    "parameters": str(tool["signature"])
                }
            else:
                return {"error": f"Tool {tool_name} not found"}
        
        # Return all tool descriptions
        return {
            name: {
                "description": tool["description"],
                "parameters": str(tool["signature"])
            }
            for name, tool in self.tools.items()
        }
    
    def get_agent_history(self, agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get history of tool calls for a specific agent or all agents.
        
        Args:
            agent_name: Name of agent to get history for (None returns all)
            
        Returns:
            List of historical tool calls
        """
        if agent_name is None:
            return self.history
        
        return [entry for entry in self.history if entry["agent"] == agent_name]
    
    def broadcast_message(self, sender: str, message: str, recipients: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Broadcast a message to other agents.
        
        Args:
            sender: Agent sending the message
            message: Message content
            recipients: List of recipient agents (None broadcasts to all)
            
        Returns:
            Broadcast result
        """
        if recipients is None:
            recipients = [name for name in self.registered_agents.keys() if name != sender]
        
        logger.info(f"Agent {sender} broadcasting message to {len(recipients)} agents")
        
        # Store the message in context for other agents to access
        message_key = f"message_{sender}_{logging.Formatter.converter()[0]}"
        self.update_context(message_key, {
            "sender": sender,
            "message": message,
            "recipients": recipients,
            "read_by": []
        })
        
        return {
            "status": "message_broadcast",
            "message_id": message_key,
            "recipients": recipients
        }
    
    def get_messages(self, agent_name: str) -> List[Dict[str, Any]]:
        """
        Get messages for a specific agent.
        
        Args:
            agent_name: Name of agent to get messages for
            
        Returns:
            List of messages for the agent
        """
        messages = []
        
        for key, value in self.context.items():
            if key.startswith("message_") and isinstance(value, dict):
                if agent_name in value.get("recipients", []) and agent_name not in value.get("read_by", []):
                    messages.append(value)
                    # Mark as read
                    value.setdefault("read_by", []).append(agent_name)
        
        return messages
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current status of the MCP system.
        
        Returns:
            System status information
        """
        return {
            "registered_agents": list(self.registered_agents.keys()),
            "registered_tools": list(self.tools.keys()),
            "context_keys": list(self.context.keys()),
            "history_entries": len(self.history),
            "status": "active"
        } 