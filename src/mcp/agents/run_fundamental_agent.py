#!/usr/bin/env python
"""
Script to run the Fundamental Analysis Agent with Model Context Protocol integration.
This agent analyzes fundamental financial data and generates long-term trading signals.
"""

import logging
import time
import signal
import sys
import argparse
from typing import List, Dict, Any

from src.agents.trading.fundamental_agent import FundamentalAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("fundamental_agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global flag for shutdown
shutdown_requested = False

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Fundamental Analysis Agent with MCP")
    parser.add_argument("--mcp-server", default="http://localhost:5000", 
                        help="URL of the MCP server")
    parser.add_argument("--api-key", default=None,
                        help="API key for MCP server authentication")
    parser.add_argument("--tickers", nargs="+", 
                        default=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
                        help="List of ticker symbols to analyze")
    parser.add_argument("--interval", type=int, default=3600,
                        help="Interval in seconds between analyses (default: 3600)")
    return parser.parse_args()

def handle_shutdown(signum, frame):
    """Handle shutdown signals."""
    global shutdown_requested
    logger.info("Shutdown requested, will exit after current operation...")
    shutdown_requested = True

def fetch_financial_data(agent: FundamentalAgent, ticker: str) -> Dict[str, Any]:
    """
    Fetch financial data for a ticker using MCP tools.
    
    Args:
        agent: FundamentalAgent instance
        ticker: Ticker symbol
        
    Returns:
        Dict containing financial data
    """
    try:
        # In a real implementation, we would fetch actual financial data
        # For this demo, we'll generate mock financial data
        
        # Use MCP to get market data first
        market_data = agent.call_tool("fetch_market_data", ticker=ticker, lookback_days=365)
        if "error" in market_data:
            logger.error(f"Error fetching market data for {ticker}: {market_data['error']}")
            return generate_mock_financial_data(ticker)
        
        # Generate financial metrics based on the market data
        current_price = market_data.get("close", 100)
        
        # Generate realistic financial data
        return {
            "ticker": ticker,
            "valuation_metrics": {
                "pe_ratio": current_price / (current_price * 0.05),  # 5% earnings yield
                "price_to_book": current_price / (current_price * 0.3),  # Book value at 30% of price
                "price_to_sales": current_price / (current_price * 0.2),  # Sales at 20% of price
                "ev_to_ebitda": 10 + (market_data.get("volatility", 0.1) * 10)  # Higher volatility, higher multiple
            },
            "growth_rates": {
                "revenue_growth": 0.15 + (market_data.get("trend", 0) * 0.1),  # Base + trend adjustment
                "earnings_growth": 0.10 + (market_data.get("trend", 0) * 0.2),  # Base + trend adjustment
                "dividend_growth": 0.05 if market_data.get("trend", 0) > 0 else 0.02  # Higher in uptrend
            },
            "financial_health": {
                "debt_to_equity": 1.5 - (market_data.get("trend", 0) * 0.5),  # Lower in uptrend
                "current_ratio": 1.8 + (market_data.get("trend", 0) * 0.3),  # Higher in uptrend
                "quick_ratio": 1.2 + (market_data.get("trend", 0) * 0.2)  # Higher in uptrend
            },
            "market_position": {
                "market_share": 0.1 + (abs(market_data.get("trend", 0)) * 0.1),  # Higher with stronger trend
                "competitive_advantage": 0.6 + (market_data.get("trend", 0) * 0.1),  # Higher in uptrend
                "industry_outlook": 0.5 + (market_data.get("trend", 0) * 0.2)  # Better outlook in uptrend
            }
        }
    
    except Exception as e:
        logger.error(f"Error fetching financial data for {ticker}: {e}")
        return generate_mock_financial_data(ticker)

def generate_mock_financial_data(ticker: str) -> Dict[str, Any]:
    """Generate mock financial data if unable to fetch real data."""
    import random
    
    # Generate random but reasonable financial data
    trend = random.uniform(-0.2, 0.2)
    
    return {
        "ticker": ticker,
        "valuation_metrics": {
            "pe_ratio": max(8, min(30, 15 + trend * 20)),
            "price_to_book": max(1, min(5, 2.5 + trend * 3)),
            "price_to_sales": max(0.5, min(10, 3 + trend * 5)),
            "ev_to_ebitda": max(5, min(20, 10 + trend * 8))
        },
        "growth_rates": {
            "revenue_growth": max(-0.1, min(0.3, 0.1 + trend * 0.2)),
            "earnings_growth": max(-0.15, min(0.35, 0.08 + trend * 0.25)),
            "dividend_growth": max(0, min(0.1, 0.03 + trend * 0.07))
        },
        "financial_health": {
            "debt_to_equity": max(0.5, min(3, 1.5 - trend)),
            "current_ratio": max(0.8, min(3, 1.8 + trend)),
            "quick_ratio": max(0.6, min(2, 1.2 + trend))
        },
        "market_position": {
            "market_share": max(0.01, min(0.3, 0.1 + abs(trend) * 0.1)),
            "competitive_advantage": max(0.2, min(0.9, 0.6 + trend * 0.2)),
            "industry_outlook": max(0.2, min(0.9, 0.5 + trend * 0.3))
        }
    }

def analyze_tickers(agent: FundamentalAgent, tickers: List[str]):
    """
    Analyze a list of tickers using the Fundamental Analysis Agent.
    
    Args:
        agent: FundamentalAgent instance
        tickers: List of ticker symbols to analyze
    """
    logger.info(f"Starting fundamental analysis for {len(tickers)} tickers")
    
    for ticker in tickers:
        if shutdown_requested:
            logger.info("Shutdown requested, stopping analysis")
            return
        
        try:
            logger.info(f"Analyzing {ticker}")
            
            # Fetch financial data for the ticker
            financial_data = fetch_financial_data(agent, ticker)
            
            # Analyze the data
            result = agent.analyze(financial_data)
            
            # Log the results
            logger.info(f"Analysis for {ticker}: {result['action']} with confidence {result['confidence']}")
            logger.info(f"Rationale: {result['rationale']}")
            logger.info(f"Component scores: {result['component_scores']}")
            
        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {e}")

def main():
    """Main execution function."""
    args = parse_args()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    try:
        # Create agent
        logger.info(f"Creating Fundamental Analysis Agent with MCP server at {args.mcp_server}")
        agent = FundamentalAgent(
            mcp_server_url=args.mcp_server,
            api_key=args.api_key
        )
        
        # Main loop
        while not shutdown_requested:
            analyze_tickers(agent, args.tickers)
            
            # Sleep until next interval
            logger.info(f"Analysis complete. Sleeping for {args.interval} seconds...")
            for _ in range(args.interval):
                if shutdown_requested:
                    break
                time.sleep(1)
        
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
    
    logger.info("Fundamental Analysis Agent shutting down")
    sys.exit(0)

if __name__ == "__main__":
    main() 