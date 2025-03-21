"""
Base agent class that implements common functionality for all trading agents.
Includes MCP integration for tool calling and agent communication.
"""
import logging
import time
from typing import Dict, Any, Optional, List, Union

# Import MCP client to interact with the Model Context Protocol server
from src.agents.mcp_client import MCPClient

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base agent class with Model Context Protocol integration."""
    
    def __init__(self, 
                 name: str,
                 mcp_server_url: str,
                 api_key: Optional[str] = None,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the base agent.
        
        Args:
            name: Name of the agent
            mcp_server_url: URL of the MCP server
            api_key: Optional API key for authentication
            config: Optional configuration settings
        """
        self.name = name
        self.config = config or {}
        
        # Initialize MCP client
        self.mcp = MCPClient(mcp_server_url, api_key=api_key)
        self.mcp_server_url = mcp_server_url
        
        logger.info(f"Initialized agent: {self.name}")
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Call a tool registered with the MCP server.
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Arguments to pass to the tool
            
        Returns:
            Tool response as a dictionary
        """
        try:
            logger.debug(f"Agent {self.name} calling tool: {tool_name}")
            response = self.mcp.call_tool(tool_name, **kwargs)
            
            if isinstance(response, dict) and "error" in response:
                logger.error(f"Error calling tool {tool_name}: {response['error']}")
            
            return response
        
        except Exception as e:
            logger.error(f"Exception when calling tool {tool_name}: {e}")
            return {"error": str(e)}
    
    def send_message(self, message: str, recipients: List[str]) -> Dict[str, Any]:
        """
        Send a message to other agents through MCP.
        
        Args:
            message: Message content
            recipients: List of recipient agent names
            
        Returns:
            Response from the MCP server
        """
        try:
            msg_data = {
                "sender": self.name,
                "recipients": recipients,
                "message": message,
                "timestamp": int(time.time())
            }
            
            logger.info(f"Agent {self.name} sending message to {recipients}: {message}")
            return self.mcp.set_context(f"message_{int(time.time())}", msg_data)
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return {"error": str(e)}
    
    def handle_message(self, message: Dict[str, Any]) -> None:
        """
        Handle an incoming message from another agent.
        Base implementation logs the message, override for specific behavior.
        
        Args:
            message: Message from another agent
        """
        sender = message.get("sender", "Unknown")
        content = message.get("message", "")
        
        logger.info(f"Agent {self.name} received message from {sender}: {content}")
    
    def store_signal(self, signal: Dict[str, Any]) -> None:
        """
        Store a trading signal in the MCP context for other agents to access.
        
        Args:
            signal: Trading signal to store
        """
        try:
            # Add agent type and timestamp
            signal_data = signal.copy()
            
            # Extract agent type from name
            agent_type = "unknown"
            if "Technical" in self.name:
                agent_type = "technical"
            elif "Fundamental" in self.name:
                agent_type = "fundamental"
            elif "Sentiment" in self.name:
                agent_type = "sentiment"
            
            signal_data["agent_type"] = agent_type
            
            if "timestamp" not in signal_data:
                signal_data["timestamp"] = int(time.time())
            
            # Create a unique key for the signal
            ticker = signal.get("ticker", "UNKNOWN")
            key = f"signal_{self.name}_{ticker}_{signal_data['timestamp']}"
            
            logger.info(f"Agent {self.name} storing signal for {ticker}: {signal['action']}")
            return self.mcp.set_context(key, signal_data)
            
        except Exception as e:
            logger.error(f"Error storing signal: {e}")
            return {"error": str(e)}
    
    def check_messages(self) -> List[Dict[str, Any]]:
        """
        Check for messages sent to this agent.
        
        Returns:
            List of messages for this agent
        """
        try:
            context = self.mcp.get_context()
            if "error" in context:
                logger.error(f"Error getting context: {context['error']}")
                return []
            
            messages = []
            for key, value in context.items():
                if (key.startswith("message_") and 
                    isinstance(value, dict) and
                    "recipients" in value and
                    (self.name in value["recipients"] or "all" in value["recipients"])):
                    messages.append(value)
            
            # Sort by timestamp, newest first
            messages.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
            return messages
            
        except Exception as e:
            logger.error(f"Error checking messages: {e}")
            return []
    
    def get_recent_signals(self, ticker: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get recent trading signals from the MCP context.
        
        Args:
            ticker: Optional ticker to filter signals by
            
        Returns:
            List of trading signals
        """
        try:
            context = self.mcp.get_context()
            if "error" in context:
                logger.error(f"Error getting context: {context['error']}")
                return []
            
            signals = []
            for key, value in context.items():
                if (key.startswith("signal_") and 
                    isinstance(value, dict) and
                    "action" in value and
                    (ticker is None or value.get("ticker") == ticker)):
                    signals.append(value)
            
            # Sort by timestamp, newest first
            signals.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
            return signals
            
        except Exception as e:
            logger.error(f"Error getting recent signals: {e}")
            return []
    
    def analyze(self, data: Any) -> Dict[str, Any]:
        """
        Analyze data and generate a trading signal.
        This is a placeholder method that should be overridden by subclasses.
        
        Args:
            data: Data to analyze
            
        Returns:
            Trading signal as a dictionary
        """
        raise NotImplementedError("Subclasses must implement analyze()")
    
    def process_messages(self) -> None:
        """Process incoming messages from other agents."""
        messages = self.check_messages()
        
        for message in messages:
            self.handle_message(message)
    
    def run_cycle(self, data: Any) -> Dict[str, Any]:
        """
        Run a full agent cycle: process messages, analyze data, store signal.
        
        Args:
            data: Data to analyze
            
        Returns:
            Trading signal generated by the agent
        """
        # Process any incoming messages
        self.process_messages()
        
        # Analyze data and generate signal
        signal = self.analyze(data)
        
        # Store the signal in MCP context
        self.store_signal(signal)
        
        return signal 