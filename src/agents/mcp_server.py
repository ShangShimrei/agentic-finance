"""
Model Context Protocol (MCP) server that provides an API for agent communication.
"""
import logging
import json
import time
from typing import Dict, Any, List, Optional, Callable, Set
from pathlib import Path
import threading
import inspect
import uuid
from flask import Flask, request, jsonify
from werkzeug.serving import make_server

logger = logging.getLogger(__name__)

class ModelContextProtocolServer:
    """
    Model Context Protocol (MCP) server that manages context and coordinates tool calls across agents.
    Provides HTTP API endpoints for clients to interact with.
    """
    
    def __init__(self, host: str = 'localhost', port: int = 5000, auth_enabled: bool = False):
        """
        Initialize the Model Context Protocol server.
        
        Args:
            host: Host address to bind the server
            port: Port number to run the server on
            auth_enabled: Whether to enable API key authentication
        """
        self.host = host
        self.port = port
        self.auth_enabled = auth_enabled
        self.api_keys: Dict[str, str] = {}  # agent_name -> api_key mapping
        
        self.context: Dict[str, Any] = {}
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.registered_agents: Set[str] = set()
        self.history: List[Dict[str, Any]] = []
        self.message_queue: Dict[str, List[Dict[str, Any]]] = {}
        
        # Create Flask app
        self.app = Flask("ModelContextProtocol")
        self._setup_routes()
        
        self.server = None
        self.server_thread = None
        
        logger.info(f"Initializing Model Context Protocol server on {host}:{port}")
    
    def _setup_routes(self) -> None:
        """Set up API routes for the Flask app."""
        # Tool routes
        self.app.route('/tools/<tool_name>', methods=['POST'])(self._handle_tool_call)
        self.app.route('/tools', methods=['GET'])(self._handle_get_tools)
        self.app.route('/tools/<tool_name>', methods=['GET'])(self._handle_get_tool_description)
        
        # Context routes
        self.app.route('/context', methods=['GET'])(self._handle_get_all_context)
        self.app.route('/context/<key>', methods=['GET'])(self._handle_get_context)
        self.app.route('/context/<key>', methods=['PUT'])(self._handle_update_context)
        
        # Message routes
        self.app.route('/messages/broadcast', methods=['POST'])(self._handle_broadcast_message)
        self.app.route('/messages', methods=['GET'])(self._handle_get_messages)
        
        # Agent routes
        self.app.route('/agents/register', methods=['POST'])(self._handle_register_agent)
        
        # Status route
        self.app.route('/status', methods=['GET'])(self._handle_get_status)
    
    def start(self) -> None:
        """Start the MCP server."""
        if self.server:
            logger.warning("Server already running")
            return
        
        # Create server in a separate thread
        self.server = make_server(self.host, self.port, self.app)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        logger.info(f"MCP server started at http://{self.host}:{self.port}")
    
    def stop(self) -> None:
        """Stop the MCP server."""
        if self.server:
            self.server.shutdown()
            self.server = None
            self.server_thread = None
            logger.info("MCP server stopped")
    
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
    
    def register_api_key(self, agent_name: str, api_key: Optional[str] = None) -> str:
        """
        Register an API key for an agent.
        
        Args:
            agent_name: Name of the agent
            api_key: Optional API key (generates one if not provided)
            
        Returns:
            The API key
        """
        if not api_key:
            api_key = str(uuid.uuid4())
        
        self.api_keys[agent_name] = api_key
        return api_key
    
    def _verify_auth(self, request_obj) -> bool:
        """
        Verify authentication for a request.
        
        Args:
            request_obj: The Flask request object
            
        Returns:
            True if authentication is successful or disabled
        """
        if not self.auth_enabled:
            return True
        
        auth_header = request_obj.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False
        
        api_key = auth_header[7:]  # Remove 'Bearer ' prefix
        agent_name = request_obj.json.get('agent_name') or request_obj.args.get('agent_name')
        
        if not agent_name or agent_name not in self.api_keys:
            return False
        
        return self.api_keys[agent_name] == api_key
    
    def _log_request(self, agent_name: str, endpoint: str, method: str) -> None:
        """
        Log an API request.
        
        Args:
            agent_name: Name of the agent making the request
            endpoint: API endpoint
            method: HTTP method
        """
        logger.debug(f"Request: {method} {endpoint} from {agent_name}")
    
    # Flask route handlers
    def _handle_tool_call(self, tool_name: str):
        """Handle a tool call request."""
        if self.auth_enabled and not self._verify_auth(request):
            return jsonify({"error": "Unauthorized"}), 401
        
        data = request.json
        agent_name = data.get('agent_name')
        arguments = data.get('arguments', {})
        
        self._log_request(agent_name, f"/tools/{tool_name}", "POST")
        
        if tool_name not in self.tools:
            return jsonify({"error": f"Tool {tool_name} not found"}), 404
        
        tool = self.tools[tool_name]
        
        try:
            # Execute the tool
            result = tool["function"](**arguments)
            
            # Record the call in history
            self.history.append({
                "timestamp": time.time(),
                "agent": agent_name,
                "tool": tool_name,
                "arguments": arguments,
                "status": "success"
            })
            
            return jsonify(result)
        
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            
            # Record the failed call
            self.history.append({
                "timestamp": time.time(),
                "agent": agent_name,
                "tool": tool_name,
                "arguments": arguments,
                "status": "error",
                "error": str(e)
            })
            
            return jsonify({"error": str(e)}), 500
    
    def _handle_get_tools(self):
        """Handle a request to get all tool descriptions."""
        if self.auth_enabled and not self._verify_auth(request):
            return jsonify({"error": "Unauthorized"}), 401
        
        agent_name = request.args.get('agent_name', 'Unknown')
        self._log_request(agent_name, "/tools", "GET")
        
        # Return all tool descriptions
        tools_info = {
            name: {
                "description": tool["description"],
                "parameters": str(tool["signature"])
            }
            for name, tool in self.tools.items()
        }
        
        return jsonify(tools_info)
    
    def _handle_get_tool_description(self, tool_name: str):
        """Handle a request to get a specific tool description."""
        if self.auth_enabled and not self._verify_auth(request):
            return jsonify({"error": "Unauthorized"}), 401
        
        agent_name = request.args.get('agent_name', 'Unknown')
        self._log_request(agent_name, f"/tools/{tool_name}", "GET")
        
        if tool_name in self.tools:
            tool = self.tools[tool_name]
            return jsonify({
                "name": tool_name,
                "description": tool["description"],
                "parameters": str(tool["signature"])
            })
        else:
            return jsonify({"error": f"Tool {tool_name} not found"}), 404
    
    def _handle_get_all_context(self):
        """Handle a request to get all context."""
        if self.auth_enabled and not self._verify_auth(request):
            return jsonify({"error": "Unauthorized"}), 401
        
        agent_name = request.args.get('agent_name', 'Unknown')
        self._log_request(agent_name, "/context", "GET")
        
        return jsonify(self.context)
    
    def _handle_get_context(self, key: str):
        """Handle a request to get a specific context value."""
        if self.auth_enabled and not self._verify_auth(request):
            return jsonify({"error": "Unauthorized"}), 401
        
        agent_name = request.args.get('agent_name', 'Unknown')
        self._log_request(agent_name, f"/context/{key}", "GET")
        
        if key in self.context:
            return jsonify(self.context[key])
        else:
            return jsonify({"error": f"Context key {key} not found"}), 404
    
    def _handle_update_context(self, key: str):
        """Handle a request to update context."""
        if self.auth_enabled and not self._verify_auth(request):
            return jsonify({"error": "Unauthorized"}), 401
        
        data = request.json
        agent_name = data.get('agent_name', 'Unknown')
        value = data.get('value')
        
        self._log_request(agent_name, f"/context/{key}", "PUT")
        
        self.context[key] = value
        logger.info(f"Agent {agent_name} updated context: {key}")
        
        return jsonify({"status": "success", "key": key})
    
    def _handle_broadcast_message(self):
        """Handle a request to broadcast a message."""
        if self.auth_enabled and not self._verify_auth(request):
            return jsonify({"error": "Unauthorized"}), 401
        
        data = request.json
        sender = data.get('sender', 'Unknown')
        message = data.get('message', '')
        recipients = data.get('recipients')
        
        self._log_request(sender, "/messages/broadcast", "POST")
        
        if recipients is None:
            recipients = [name for name in self.registered_agents if name != sender]
        
        logger.info(f"Agent {sender} broadcasting message to {len(recipients)} agents")
        
        # Store the message in queues for recipients
        message_id = str(uuid.uuid4())
        message_data = {
            "id": message_id,
            "sender": sender,
            "message": message,
            "timestamp": time.time()
        }
        
        for recipient in recipients:
            if recipient not in self.message_queue:
                self.message_queue[recipient] = []
            
            self.message_queue[recipient].append(message_data)
        
        return jsonify({
            "status": "message_broadcast",
            "message_id": message_id,
            "recipients": recipients
        })
    
    def _handle_get_messages(self):
        """Handle a request to get messages for an agent."""
        if self.auth_enabled and not self._verify_auth(request):
            return jsonify({"error": "Unauthorized"}), 401
        
        agent_name = request.args.get('agent_name')
        self._log_request(agent_name, "/messages", "GET")
        
        if not agent_name:
            return jsonify({"error": "Missing agent_name parameter"}), 400
        
        # Get messages for the agent and clear the queue
        messages = self.message_queue.get(agent_name, [])
        self.message_queue[agent_name] = []
        
        return jsonify(messages)
    
    def _handle_register_agent(self):
        """Handle a request to register an agent."""
        data = request.json
        agent_name = data.get('agent_name')
        
        if not agent_name:
            return jsonify({"error": "Missing agent_name parameter"}), 400
        
        self._log_request(agent_name, "/agents/register", "POST")
        
        # Add to registered agents
        self.registered_agents.add(agent_name)
        logger.info(f"Registered agent: {agent_name}")
        
        # Initialize message queue for the agent
        if agent_name not in self.message_queue:
            self.message_queue[agent_name] = []
        
        return jsonify({
            "status": "agent_registered",
            "agent_name": agent_name,
            "registered_at": time.time()
        })
    
    def _handle_get_status(self):
        """Handle a request to get system status."""
        if self.auth_enabled and not self._verify_auth(request):
            return jsonify({"error": "Unauthorized"}), 401
        
        agent_name = request.args.get('agent_name', 'Unknown')
        self._log_request(agent_name, "/status", "GET")
        
        return jsonify({
            "registered_agents": list(self.registered_agents),
            "registered_tools": list(self.tools.keys()),
            "context_keys": list(self.context.keys()),
            "history_entries": len(self.history),
            "status": "active",
            "timestamp": time.time()
        }) 