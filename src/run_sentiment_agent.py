#!/usr/bin/env python
"""
Script to run the Sentiment Analysis Agent with Model Context Protocol integration.
This agent analyzes news, social media, and other sentiment sources for trading signals.
"""

import logging
import time
import signal
import sys
import argparse
from typing import List

from src.agents.trading.sentiment_agent import SentimentAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sentiment_agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global flag for shutdown
shutdown_requested = False

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Sentiment Analysis Agent with MCP")
    parser.add_argument("--mcp-server", default="http://localhost:5000", 
                        help="URL of the MCP server")
    parser.add_argument("--api-key", default=None,
                        help="API key for MCP server authentication")
    parser.add_argument("--tickers", nargs="+", 
                        default=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
                        help="List of ticker symbols to analyze")
    parser.add_argument("--interval", type=int, default=1800,
                        help="Interval in seconds between analyses (default: 1800)")
    return parser.parse_args()

def handle_shutdown(signum, frame):
    """Handle shutdown signals."""
    global shutdown_requested
    logger.info("Shutdown requested, will exit after current operation...")
    shutdown_requested = True

def analyze_tickers(agent: SentimentAgent, tickers: List[str]):
    """
    Analyze sentiment for a list of tickers.
    
    Args:
        agent: SentimentAgent instance
        tickers: List of ticker symbols to analyze
    """
    logger.info(f"Starting sentiment analysis for {len(tickers)} tickers")
    
    for ticker in tickers:
        if shutdown_requested:
            logger.info("Shutdown requested, stopping analysis")
            return
        
        try:
            logger.info(f"Analyzing sentiment for {ticker}")
            
            # Analyze the ticker's sentiment
            result = agent.analyze(ticker)
            
            # Log the results
            logger.info(f"Sentiment analysis for {ticker}: {result['action']} with confidence {result['confidence']}")
            logger.info(f"Sentiment score: {result['sentiment_score']}")
            logger.info(f"Rationale: {result['rationale']}")
            
            if result.get("topics"):
                logger.info(f"Topics: {', '.join(result['topics'])}")
            
            # Brief pause between tickers to avoid overwhelming API
            time.sleep(1)
            
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
        logger.info(f"Creating Sentiment Analysis Agent with MCP server at {args.mcp_server}")
        agent = SentimentAgent(
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
    
    logger.info("Sentiment Analysis Agent shutting down")
    sys.exit(0)

if __name__ == "__main__":
    main() 