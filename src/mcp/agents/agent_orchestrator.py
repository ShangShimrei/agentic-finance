"""
Agent Orchestrator that coordinates the operation of multiple trading agents.
"""
import logging
from typing import Dict, Any, List, Optional
import importlib
import inspect

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Coordinates multiple trading agents to analyze market data and generate trading signals.
    """
    
    def __init__(self, agent_configs: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the Agent Orchestrator.
        
        Args:
            agent_configs: List of agent configurations with the following format:
                [
                    {
                        "name": "BuffetAgent",
                        "module": "src.agents.trading",
                        "class": "BuffetAgent",
                        "weight": 1.0,
                        "params": {}  # Constructor parameters for the agent
                    },
                    ...
                ]
        """
        self.agents = []
        self.agent_weights = {}
        
        if agent_configs:
            self.load_agents(agent_configs)
        
        logger.info(f"Initialized Agent Orchestrator with {len(self.agents)} agents")
    
    def load_agents(self, agent_configs: List[Dict[str, Any]]) -> None:
        """
        Load and initialize trading agents based on configurations.
        
        Args:
            agent_configs: List of agent configurations
        """
        for config in agent_configs:
            name = config.get("name")
            module_name = config.get("module")
            class_name = config.get("class")
            weight = config.get("weight", 1.0)
            params = config.get("params", {})
            
            if not all([name, module_name, class_name]):
                logger.warning(f"Skipping invalid agent config: {config}")
                continue
            
            try:
                # Import the agent module
                module = importlib.import_module(module_name)
                
                # Get the agent class
                agent_class = getattr(module, class_name)
                
                # Create the agent instance
                agent = agent_class(**params)
                
                # Store the agent with its weight
                self.agents.append(agent)
                self.agent_weights[agent] = weight
                
                logger.info(f"Loaded agent: {name} with weight {weight}")
            except (ImportError, AttributeError, TypeError) as e:
                logger.error(f"Failed to load agent {name}: {e}")
    
    def add_agent(self, agent, weight: float = 1.0) -> None:
        """
        Add a trading agent to the orchestrator.
        
        Args:
            agent: Trading agent instance
            weight: Weight factor for the agent's signals
        """
        self.agents.append(agent)
        self.agent_weights[agent] = weight
        logger.info(f"Added agent: {agent.__class__.__name__} with weight {weight}")
    
    def remove_agent(self, agent_name: str) -> bool:
        """
        Remove a trading agent from the orchestrator.
        
        Args:
            agent_name: Name of the agent to remove
            
        Returns:
            True if agent was removed, False otherwise
        """
        for agent in self.agents:
            if agent.__class__.__name__ == agent_name:
                self.agents.remove(agent)
                self.agent_weights.pop(agent, None)
                logger.info(f"Removed agent: {agent_name}")
                return True
        
        logger.warning(f"Agent not found: {agent_name}")
        return False
    
    def get_agents(self) -> List[Any]:
        """
        Get the list of all agents.
        
        Returns:
            List of agent instances
        """
        return self.agents
    
    def analyze_market_data(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Run analysis on market data using all registered agents.
        
        Args:
            market_data: Market data to analyze
            
        Returns:
            List of trading signals from all agents
        """
        ticker = market_data.get("ticker", "UNKNOWN")
        logger.info(f"Analyzing market data for {ticker} with {len(self.agents)} agents")
        
        trading_signals = []
        
        for agent in self.agents:
            try:
                # Check if the agent has an analyze method
                if hasattr(agent, "analyze") and callable(getattr(agent, "analyze")):
                    # Get the signal
                    signal = agent.analyze(market_data)
                    
                    # Add agent information to the signal
                    signal["agent"] = agent.__class__.__name__
                    signal["weight"] = self.agent_weights.get(agent, 1.0)
                    
                    # Add ticker if not present
                    if "ticker" not in signal:
                        signal["ticker"] = ticker
                    
                    trading_signals.append(signal)
                else:
                    logger.warning(f"Agent {agent.__class__.__name__} does not have analyze method")
            except Exception as e:
                logger.error(f"Error running agent {agent.__class__.__name__}: {e}")
        
        logger.info(f"Generated {len(trading_signals)} trading signals for {ticker}")
        return trading_signals 