#!/usr/bin/env python
"""
Script to run the Model Context Protocol (MCP) server and register tools.
"""
import logging
import time
import signal
import sys
from pathlib import Path
from typing import Dict, Any

from src.agents.mcp_server import ModelContextProtocolServer
from src.agents.mcp_tools import (
    calculate_indicators,
    fetch_market_data,
    analyze_sentiment,
    generate_trade_recommendation,
    fetch_news
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mcp_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def register_tools(server: ModelContextProtocolServer) -> None:
    """
    Register all available tools with the MCP server.
    
    Args:
        server: MCP server instance
    """
    # Register technical analysis tools
    server.register_tool(
        "calculate_indicators",
        calculate_indicators,
        "Calculate technical indicators from price history"
    )
    
    # Register market data tools
    server.register_tool(
        "fetch_market_data",
        fetch_market_data,
        "Fetch market data for a ticker"
    )
    
    # Register news API tools
    server.register_tool(
        "fetch_news",
        fetch_news,
        "Fetch news articles for a ticker"
    )
    
    # Register sentiment analysis tools
    server.register_tool(
        "analyze_sentiment",
        analyze_sentiment,
        "Analyze market sentiment for a ticker"
    )
    
    # Register trade recommendation tools
    server.register_tool(
        "generate_trade_recommendation",
        generate_trade_recommendation,
        "Generate a trade recommendation based on multiple signals"
    )
    
    logger.info("Registered all tools with MCP server")

def handle_shutdown(signum, frame):
    """Handle shutdown signal."""
    logger.info("Received shutdown signal")
    if 'mcp_server' in globals():
        logger.info("Stopping MCP server")
        mcp_server.stop()
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    try:
        # Create and start MCP server
        mcp_server = ModelContextProtocolServer(host='localhost', port=5000)
        
        # Register tools
        register_tools(mcp_server)
        
        # Start the server
        mcp_server.start()
        
        logger.info("MCP server started successfully at http://localhost:5000")
        logger.info("Press Ctrl+C to stop the server")
        
        # Keep the main thread running
        while True:
            time.sleep(1)
    
    except Exception as e:
        logger.error(f"Error starting MCP server: {e}")
        if 'mcp_server' in locals():
            mcp_server.stop()
        sys.exit(1) 