#!/usr/bin/env python3
import os
import json
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import agent modules
from agents.buffet_agent import BuffetAgent
from agents.ackman_agent import AckmanAgent
from agents.fundamental_agent import FundamentalAgent
from agents.sentiment_agent import SentimentAgent
from agents.technical_agent import TechnicalAgent
from agents.valuation_agent import ValuationAgent

# Import other system components
from risk_manager.risk_manager import RiskManager
from portfolio_manager.portfolio_manager import PortfolioManager
from execution.execution import ExecutionEngine
from visualization.visualizer import Visualizer
from research.research_agent import ResearchAgent
from api.api import create_api

def load_config():
    """Load configuration from config file."""
    config_path = Path(__file__).parent.parent / 'config' / 'config.json'
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise

def initialize_agents(config):
    """Initialize all trading agents based on configuration."""
    agents = {}
    
    if config['agents']['buffet']['active']:
        agents['buffet'] = BuffetAgent(config)
        
    if config['agents']['ackman']['active']:
        agents['ackman'] = AckmanAgent(config)
        
    if config['agents']['fundamental']['active']:
        agents['fundamental'] = FundamentalAgent(config)
        
    if config['agents']['sentiment']['active']:
        agents['sentiment'] = SentimentAgent(config)
        
    if config['agents']['technical']['active']:
        agents['technical'] = TechnicalAgent(config)
        
    if config['agents']['valuation']['active']:
        agents['valuation'] = ValuationAgent(config)
    
    return agents

def main():
    """Main entry point for the application."""
    logger.info("Starting Agentic Finance Prototype")
    
    # Load configuration
    config = load_config()
    logger.info(f"Loaded configuration for {len(config['symbols'])} symbols")
    
    # Initialize components
    agents = initialize_agents(config)
    logger.info(f"Initialized {len(agents)} trading agents")
    
    risk_manager = RiskManager(config)
    portfolio_manager = PortfolioManager(config)
    execution_engine = ExecutionEngine(config)
    visualizer = Visualizer(config)
    research_agent = ResearchAgent(config)
    
    # Start API server
    api = create_api(
        agents=agents,
        risk_manager=risk_manager,
        portfolio_manager=portfolio_manager,
        execution_engine=execution_engine,
        visualizer=visualizer,
        research_agent=research_agent,
        config=config
    )
    
    logger.info("System initialized successfully")
    
    # Here you would typically start the API server
    # api.run(host='0.0.0.0', port=5000)
    
    logger.info("API server started")
    
    # For now, just run a simple test cycle
    logger.info("Running test trading cycle")
    run_test_cycle(agents, risk_manager, portfolio_manager, execution_engine, visualizer, research_agent, config)

def run_test_cycle(agents, risk_manager, portfolio_manager, execution_engine, visualizer, research_agent, config):
    """Run a simple test cycle to demonstrate the system flow."""
    # Get trading signals from agents
    signals = {}
    for name, agent in agents.items():
        signals[name] = agent.generate_signal(config['symbols'])
    
    # Process signals through risk manager
    risk_adjusted_signals = risk_manager.process_signals(signals)
    
    # Portfolio manager determines actions
    portfolio_actions = portfolio_manager.determine_actions(risk_adjusted_signals)
    
    # Execute actions
    execution_results = execution_engine.execute_actions(portfolio_actions)
    
    # Visualize results
    visualizer.visualize_cycle(signals, risk_adjusted_signals, portfolio_actions, execution_results)
    
    # Research agent analyzes cycle
    insights = research_agent.analyze_cycle(signals, risk_adjusted_signals, portfolio_actions, execution_results)
    
    return execution_results

if __name__ == "__main__":
    main()
