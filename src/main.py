"""
Main entry point for the Agentic Hedge Fund application.
"""
import logging
import argparse
import sys
from datetime import datetime, timedelta
import signal
import json

from src.agents.agent_orchestrator import AgentOrchestrator
from src.agents.model_context_protocol import ModelContextProtocol
from src.risk_manager import RiskManager
from src.portfolio.portfolio_manager import PortfolioManager
from src.data_providers.market_data import MarketDataProvider
from src.simulator.trading_simulator import TradingSimulator
from src.actions.order_executor import OrderExecutor
from src.frontend.dashboard import TradingDashboard
from src.frontend.landing_page_server import LandingPageServer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('trading_app.log')
    ]
)

logger = logging.getLogger(__name__)

def parse_args():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments object
    """
    parser = argparse.ArgumentParser(description='Agentic Hedge Fund Trading Platform')
    
    # Command subparsers
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Simulate command
    simulate_parser = subparsers.add_parser('simulate', help='Run a trading simulation')
    simulate_parser.add_argument('--tickers', nargs='+', required=True, help='Tickers to simulate')
    simulate_parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD)')
    simulate_parser.add_argument('--end-date', type=str, help='End date (YYYY-MM-DD)')
    simulate_parser.add_argument('--capital', type=float, default=100000.0, help='Initial capital')
    simulate_parser.add_argument('--risk-threshold', type=float, default=0.5, help='Risk threshold (0-1)')
    simulate_parser.add_argument('--step', action='store_true', help='Run simulation step by step')
    simulate_parser.add_argument('--output', type=str, help='Output file for results')

    # Run command (for running the actual platform)
    run_parser = subparsers.add_parser('run', help='Run the trading platform')
    run_parser.add_argument('--tickers', nargs='+', required=True, help='Tickers to trade')
    run_parser.add_argument('--capital', type=float, default=100000.0, help='Initial capital')
    run_parser.add_argument('--risk-threshold', type=float, default=0.5, help='Risk threshold (0-1)')
    run_parser.add_argument('--port', type=int, default=8000, help='Web server port')
    
    # Show command (for just showing the dashboard)
    show_parser = subparsers.add_parser('show', help='Show the dashboard')
    show_parser.add_argument('--port', type=int, default=8000, help='Web server port')
    
    return parser.parse_args()

def run_simulation(args):
    """
    Run a trading simulation.
    
    Args:
        args: Command line arguments
    """
    logger.info("Setting up simulation environment")
    
    # Parse dates
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d') if args.start_date else (datetime.now() - timedelta(days=365))
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d') if args.end_date else datetime.now()
    
    # Initialize components
    mcp = ModelContextProtocol()
    market_data = MarketDataProvider()
    risk_manager = RiskManager(risk_threshold=args.risk_threshold)
    portfolio = PortfolioManager(initial_capital=args.capital)
    order_executor = OrderExecutor(is_simulation=True)
    agent_orchestrator = AgentOrchestrator(mcp=mcp)
    
    # Configure agent strategies
    agent_configs = [
        {"name": "ValueAgent", "type": "fundamental", "weight": 0.4},
        {"name": "TechnicalAgent", "type": "technical", "weight": 0.3},
        {"name": "SentimentAgent", "type": "sentiment", "weight": 0.3}
    ]
    
    # Set up the simulator
    simulator = TradingSimulator(
        tickers=args.tickers,
        start_date=start_date,
        end_date=end_date,
        market_data=market_data,
        portfolio=portfolio,
        risk_manager=risk_manager,
        order_executor=order_executor,
        agent_orchestrator=agent_orchestrator,
        agent_configs=agent_configs
    )
    
    # Set up dashboard for visualization
    dashboard = TradingDashboard(port=8080)
    dashboard.start()
    
    # Register the dashboard with the simulator
    simulator.register_dashboard(dashboard)
    
    # Run the simulation
    logger.info(f"Starting simulation for tickers: {args.tickers}")
    
    results = simulator.run_simulation(step_by_step=args.step)
    
    # Save results if output file is specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"Simulation results saved to {args.output}")
    
    # Display summary
    logger.info("Simulation completed")
    logger.info(f"Final Portfolio Value: ${results['final_portfolio_value']:.2f}")
    logger.info(f"Total Return: {results['total_return']:.2f}%")
    logger.info(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    
    # Wait for user to close dashboard
    try:
        logger.info("Press Ctrl+C to exit")
        signal.pause()
    except (KeyboardInterrupt, SystemExit):
        dashboard.stop()
        logger.info("Exiting simulation")

def run_platform(args):
    """
    Run the trading platform with live data.
    
    Args:
        args: Command line arguments
    """
    logger.info("Starting YRS Agentic Finance platform")
    
    # Initialize landing page server
    landing_page = LandingPageServer(port=args.port)
    landing_page.start()
    
    # Initialize dashboard
    dashboard = TradingDashboard(port=8080)
    dashboard.start()
    
    # Initialize platform components
    mcp = ModelContextProtocol()
    market_data = MarketDataProvider()
    risk_manager = RiskManager(risk_threshold=args.risk_threshold)
    portfolio = PortfolioManager(initial_capital=args.capital)
    order_executor = OrderExecutor(is_simulation=True)  # Set to False for live trading
    agent_orchestrator = AgentOrchestrator(mcp=mcp)
    
    # Configure agent strategies
    agent_configs = [
        {"name": "ValueAgent", "type": "fundamental", "weight": 0.4},
        {"name": "TechnicalAgent", "type": "technical", "weight": 0.3},
        {"name": "SentimentAgent", "type": "sentiment", "weight": 0.3}
    ]
    
    # Initialize agents
    for config in agent_configs:
        agent_orchestrator.add_agent(config["name"], config["type"], config["weight"])
    
    logger.info(f"Initialized with tickers: {args.tickers}")
    
    # Simulate some initial data for the dashboard
    # In a real system, this would continuously update from live market data
    sample_portfolio = {
        "cash": args.capital * 0.7,
        "positions": {
            ticker: {
                "quantity": 10, 
                "avg_price": 100.0, 
                "last_price": 105.0
            } for ticker in args.tickers
        },
        "total_value": args.capital * 1.05,
        "daily_return": 0.8,
        "total_return": 5.0,
        "initial_capital": args.capital
    }
    
    sample_trades = [
        {
            "order_id": "sample-1",
            "ticker": args.tickers[0],
            "action": "BUY",
            "order_type": "MARKET",
            "quantity": 10,
            "status": "FILLED",
            "submitted_at": datetime.now().isoformat(),
            "executed_at": datetime.now().isoformat(),
            "average_price": 100.0
        }
    ]
    
    sample_signals = [
        {
            "agent": "ValueAgent",
            "ticker": args.tickers[0],
            "action": "BUY",
            "confidence": 0.75,
            "rationale": "Undervalued based on P/E ratio",
            "time_horizon": "MEDIUM"
        }
    ]
    
    # Update dashboard
    dashboard.update_all(
        portfolio_data=sample_portfolio,
        trades_data=sample_trades,
        signals_data=sample_signals
    )
    
    # Wait for user to exit
    try:
        logger.info("YRS Agentic Finance platform is running")
        logger.info("Press Ctrl+C to exit")
        signal.pause()
    except (KeyboardInterrupt, SystemExit):
        landing_page.stop()
        dashboard.stop()
        logger.info("Shutting down YRS Agentic Finance platform")

def show_dashboard(args):
    """
    Show only the dashboard for demonstration purposes.
    
    Args:
        args: Command line arguments
    """
    logger.info("Starting YRS Agentic Finance UI")
    
    # Initialize landing page server
    landing_page = LandingPageServer(port=args.port)
    landing_page.start()
    
    # Initialize dashboard
    dashboard = TradingDashboard(port=8080)
    dashboard.start()
    
    # Simulate some data for the dashboard
    sample_portfolio = {
        "cash": 75000.0,
        "positions": {
            "AAPL": {"quantity": 50, "avg_price": 180.0, "last_price": 190.0},
            "MSFT": {"quantity": 30, "avg_price": 320.0, "last_price": 340.0},
            "GOOGL": {"quantity": 20, "avg_price": 130.0, "last_price": 135.0}
        },
        "total_value": 115000.0,
        "daily_return": 1.2,
        "total_return": 15.0,
        "initial_capital": 100000.0
    }
    
    sample_trades = [
        {
            "order_id": "demo-1",
            "ticker": "AAPL",
            "action": "BUY",
            "order_type": "MARKET",
            "quantity": 50,
            "status": "FILLED",
            "submitted_at": (datetime.now() - timedelta(days=10)).isoformat(),
            "executed_at": (datetime.now() - timedelta(days=10)).isoformat(),
            "average_price": 180.0
        },
        {
            "order_id": "demo-2",
            "ticker": "MSFT",
            "action": "BUY",
            "order_type": "MARKET",
            "quantity": 30,
            "status": "FILLED",
            "submitted_at": (datetime.now() - timedelta(days=7)).isoformat(),
            "executed_at": (datetime.now() - timedelta(days=7)).isoformat(),
            "average_price": 320.0
        },
        {
            "order_id": "demo-3",
            "ticker": "GOOGL",
            "action": "BUY",
            "order_type": "MARKET",
            "quantity": 20,
            "status": "FILLED",
            "submitted_at": (datetime.now() - timedelta(days=5)).isoformat(),
            "executed_at": (datetime.now() - timedelta(days=5)).isoformat(),
            "average_price": 130.0
        }
    ]
    
    sample_signals = [
        {
            "agent": "ValueAgent",
            "ticker": "AAPL",
            "action": "BUY",
            "confidence": 0.82,
            "rationale": "Strong earnings forecast and positive cash flow",
            "time_horizon": "LONG"
        },
        {
            "agent": "TechnicalAgent",
            "ticker": "MSFT",
            "action": "HOLD",
            "confidence": 0.65,
            "rationale": "Trading within established range, no clear breakout",
            "time_horizon": "SHORT"
        },
        {
            "agent": "SentimentAgent",
            "ticker": "GOOGL",
            "action": "BUY",
            "confidence": 0.78,
            "rationale": "Positive sentiment from recent AI announcements",
            "time_horizon": "MEDIUM"
        }
    ]
    
    # Update dashboard
    dashboard.update_all(
        portfolio_data=sample_portfolio,
        trades_data=sample_trades,
        signals_data=sample_signals
    )
    
    # Wait for user to exit
    try:
        logger.info("YRS Agentic Finance UI is running")
        logger.info("Press Ctrl+C to exit")
        signal.pause()
    except (KeyboardInterrupt, SystemExit):
        landing_page.stop()
        dashboard.stop()
        logger.info("Shutting down YRS Agentic Finance UI")

def main():
    """Main entry point of the application."""
    args = parse_args()
    
    try:
        if args.command == 'simulate':
            run_simulation(args)
        elif args.command == 'run':
            run_platform(args)
        elif args.command == 'show':
            show_dashboard(args)
        else:
            # Default to showing the dashboard if no command is provided
            logger.info("No command specified, starting UI in demonstration mode")
            show_args = argparse.Namespace()
            show_args.port = 8000
            show_dashboard(show_args)
    except Exception as e:
        logger.error(f"Error in main application: {e}", exc_info=True)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 