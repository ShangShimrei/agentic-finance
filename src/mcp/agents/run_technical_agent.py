"""
Script to run the Technical Agent with Model Context Protocol.
"""
import logging
import time
import signal
import sys
import argparse
from typing import Dict, Any, List

from src.agents.trading.technical_agent import TechnicalAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('technical_agent.log')
    ]
)

logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the Technical Agent with MCP")
    
    parser.add_argument(
        "--mcp-server",
        type=str,
        default="http://localhost:5000",
        help="URL of the MCP server"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API key for MCP server authentication"
    )
    
    parser.add_argument(
        "--tickers",
        type=str,
        nargs="+",
        default=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
        help="Ticker symbols to analyze"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Interval in seconds between analyses"
    )
    
    return parser.parse_args()

def handle_shutdown(signum, frame):
    """Handle shutdown signal."""
    logger.info("Received shutdown signal, shutting down")
    sys.exit(0)

def analyze_tickers(agent: TechnicalAgent, tickers: List[str]) -> None:
    """
    Analyze a list of tickers using the Technical Agent.
    
    Args:
        agent: Technical Agent instance
        tickers: List of ticker symbols to analyze
    """
    for ticker in tickers:
        try:
            logger.info(f"Analyzing {ticker}")
            
            # Fetch market data using MCP tool
            market_data = agent.call_tool(
                "fetch_market_data",
                ticker=ticker,
                period="1d",
                lookback=30
            )
            
            if "error" in market_data:
                logger.error(f"Error fetching data for {ticker}: {market_data['error']}")
                continue
            
            # Run analysis
            signal = agent.run(market_data)
            
            logger.info(f"Signal for {ticker}: {signal['action']} with confidence {signal['confidence']}")
            
            # Optionally, get a trade recommendation
            if signal['action'] != "HOLD" or signal['confidence'] > 0.6:
                logger.info(f"Strong signal detected for {ticker}, generating trade recommendation")
                
                # Fetch sentiment to complement technical analysis
                sentiment = agent.call_tool(
                    "analyze_sentiment",
                    ticker=ticker
                )
                
                # Include sentiment in the context
                agent.mcp.update_context(
                    f"sentiment_{ticker}_{int(time.time())}",
                    sentiment
                )
                
                # Generate and log the recommendation
                recommendation = agent.call_tool(
                    "generate_trade_recommendation",
                    ticker=ticker,
                    signals=[signal]
                )
                
                logger.info(f"Recommendation for {ticker}: {recommendation['recommendation']} with confidence {recommendation['confidence']}")
        
        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {e}")

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    try:
        # Create Technical Agent with MCP
        technical_agent = TechnicalAgent(
            mcp_server_url=args.mcp_server,
            api_key=args.api_key,
            config={
                "lookback_period": 14,
                "indicators": ["rsi", "macd", "sma", "bollinger", "price_volume"],
                "thresholds": {
                    "rsi_oversold": 30,
                    "rsi_overbought": 70,
                    "volume_significant": 1.5  # 1.5x average volume
                }
            }
        )
        
        logger.info(f"Technical Agent started, connected to MCP server at {args.mcp_server}")
        logger.info(f"Monitoring tickers: {', '.join(args.tickers)}")
        logger.info(f"Analysis interval: {args.interval} seconds")
        
        # Main loop - analyze tickers at specified interval
        while True:
            analyze_tickers(technical_agent, args.tickers)
            logger.info(f"Sleeping for {args.interval} seconds")
            time.sleep(args.interval)
    
    except Exception as e:
        logger.error(f"Error running Technical Agent: {e}")
        sys.exit(1) 