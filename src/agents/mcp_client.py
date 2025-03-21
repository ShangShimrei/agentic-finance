"""
MCP Client module for interacting with the Model Context Protocol server.
"""
import logging
import requests
import json
from typing import Dict, Any, Optional, List, Union

logger = logging.getLogger(__name__)

class MCPClient:
    """Client for interacting with the Model Context Protocol server."""
    
    def __init__(self, server_url: str, api_key: Optional[str] = None):
        """
        Initialize the MCP client.
        
        Args:
            server_url: URL of the MCP server
            api_key: Optional API key for authentication
        """
        self.server_url = server_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        
        logger.info(f"Initialized MCP client for server at {server_url}")
    
    def _make_request(self, 
                     endpoint: str, 
                     method: str = "GET", 
                     data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the MCP server.
        
        Args:
            endpoint: API endpoint to call (without leading slash)
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Optional data to send with the request
            
        Returns:
            Response from the server
        """
        url = f"{self.server_url}/{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=10)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}
            
            response.raise_for_status()
            
            if response.status_code == 204:  # No content
                return {}
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            return {"error": str(e)}
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return {"error": f"Invalid JSON in response: {e}"}
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": str(e)}
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Call a tool registered with the MCP server.
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Arguments to pass to the tool
            
        Returns:
            Tool response
        """
        data = {
            "tool": tool_name,
            "params": kwargs
        }
        
        return self._make_request("tools/call", "POST", data)
    
    def set_context(self, key: str, value: Any) -> Dict[str, Any]:
        """
        Set a key in the MCP context.
        
        Args:
            key: Context key
            value: Value to store
            
        Returns:
            Response from the server
        """
        data = {
            "key": key,
            "value": value
        }
        
        return self._make_request("context/set", "POST", data)
    
    def get_context(self, key: Optional[str] = None) -> Dict[str, Any]:
        """
        Get context from the MCP server.
        
        Args:
            key: Optional specific key to retrieve
            
        Returns:
            Context data
        """
        endpoint = "context/get"
        if key:
            endpoint += f"/{key}"
        
        return self._make_request(endpoint)
    
    def delete_context(self, key: str) -> Dict[str, Any]:
        """
        Delete a key from the MCP context.
        
        Args:
            key: Key to delete
            
        Returns:
            Response from the server
        """
        return self._make_request(f"context/delete/{key}", "DELETE")
    
    def get_tool_list(self) -> List[str]:
        """
        Get a list of available tools from the MCP server.
        
        Returns:
            List of tool names
        """
        response = self._make_request("tools/list")
        
        if "error" in response:
            return []
        
        return response.get("tools", [])
    
    def get_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """
        Get information about a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool information
        """
        return self._make_request(f"tools/info/{tool_name}")
    
    def ping(self) -> bool:
        """
        Check if the MCP server is available.
        
        Returns:
            True if server is available, False otherwise
        """
        response = self._make_request("ping")
        return "error" not in response 