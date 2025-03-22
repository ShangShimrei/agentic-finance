#!/usr/bin/env python
"""
Agent Orchestrator script that coordinates the Technical, Fundamental, and Sentiment Agents.
This orchestrator supervises the agents, combines their signals, and executes final trading decisions.
"""

import logging
import time
import signal
import sys
import argparse
from typing import List, Dict, Any, Optional
import json
import os
import subprocess
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("agent_orchestrator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global flag for shutdown
shutdown_requested = False

class AgentOrchestrator:
    """
    Agent Orchestrator that coordinates multiple trading agents.
    """
    
    def __init__(self, mcp_server_url: str, api_key: Optional[str] = None):
        """
        Initialize the Agent Orchestrator.
        
        Args:
            mcp_server_url: URL of the MCP server
            api_key: Optional API key for authentication
        """
        self.mcp_server_url = mcp_server_url
        self.api_key = api_key
        self.agents = {}
        self.agent_signals = {}
        self.decisions = {}
        self.last_check = {}
        
        logger.info(f"Initialized Agent Orchestrator with MCP server at {mcp_server_url}")
    
    def register_agent(self, agent_id: str, agent_type: str, script_path: str) -> None:
        """
        Register an agent with the orchestrator.
        
        Args:
            agent_id: Unique ID for the agent
            agent_type: Type of the agent (e.g., "technical", "fundamental")
            script_path: Path to the agent's script
        """
        self.agents[agent_id] = {
            "id": agent_id,
            "type": agent_type,
            "script_path": script_path,
            "process": None,
            "status": "stopped",
            "last_heartbeat": None,
        }
        logger.info(f"Registered agent {agent_id} of type {agent_type}")
    
    def start_agent(self, agent_id: str, args: List[str] = None) -> bool:
        """
        Start an agent with the specified ID.
        
        Args:
            agent_id: ID of the agent to start
            args: Additional command line arguments
            
        Returns:
            True if agent was started successfully, False otherwise
        """
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not registered")
            return False
        
        agent = self.agents[agent_id]
        
        if agent["status"] == "running":
            logger.warning(f"Agent {agent_id} is already running")
            return True
        
        if args is None:
            args = []
        
        # Common arguments for all agents
        cmd = [
            "python", agent["script_path"],
            "--mcp-server", self.mcp_server_url
        ]
        
        if self.api_key:
            cmd.extend(["--api-key", self.api_key])
        
        # Add any additional arguments
        cmd.extend(args)
        
        logger.info(f"Starting agent {agent_id} with command: {' '.join(cmd)}")
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
            
            agent["process"] = process
            agent["status"] = "running"
            agent["last_heartbeat"] = datetime.now()
            
            logger.info(f"Agent {agent_id} started with PID {process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start agent {agent_id}: {e}")
            agent["status"] = "error"
            return False
    
    def stop_agent(self, agent_id: str) -> bool:
        """
        Stop an agent with the specified ID.
        
        Args:
            agent_id: ID of the agent to stop
            
        Returns:
            True if agent was stopped successfully, False otherwise
        """
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not registered")
            return False
        
        agent = self.agents[agent_id]
        
        if agent["status"] != "running" or agent["process"] is None:
            logger.warning(f"Agent {agent_id} is not running")
            return True
        
        try:
            # Gracefully terminate the process
            agent["process"].terminate()
            
            # Wait up to 10 seconds for the process to terminate
            for _ in range(10):
                if agent["process"].poll() is not None:
                    break
                time.sleep(1)
            
            # Force kill if it hasn't terminated
            if agent["process"].poll() is None:
                logger.warning(f"Agent {agent_id} did not terminate gracefully, forcing kill")
                agent["process"].kill()
            
            agent["status"] = "stopped"
            agent["process"] = None
            
            logger.info(f"Agent {agent_id} stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop agent {agent_id}: {e}")
            return False
    
    def check_agent_health(self, max_heartbeat_age: int = 300) -> Dict[str, str]:
        """
        Check the health of all registered agents.
        
        Args:
            max_heartbeat_age: Maximum age of heartbeat in seconds
            
        Returns:
            Dictionary mapping agent IDs to health status
        """
        health_status = {}
        
        for agent_id, agent in self.agents.items():
            if agent["status"] != "running":
                health_status[agent_id] = agent["status"]
                continue
            
            if agent["process"] is None or agent["process"].poll() is not None:
                # Process is not running
                agent["status"] = "stopped"
                health_status[agent_id] = "stopped"
                continue
            
            # Check if we've received a heartbeat recently
            if agent["last_heartbeat"] is None:
                health_status[agent_id] = "unknown"
            elif (datetime.now() - agent["last_heartbeat"]).total_seconds() > max_heartbeat_age:
                health_status[agent_id] = "unresponsive"
            else:
                health_status[agent_id] = "healthy"
        
        return health_status
    
    def restart_unhealthy_agents(self) -> None:
        """Restart any unhealthy agents."""
        health_status = self.check_agent_health()
        
        for agent_id, status in health_status.items():
            if status in ["stopped", "error", "unresponsive"]:
                logger.warning(f"Agent {agent_id} is {status}, attempting to restart")
                self.stop_agent(agent_id)
                self.start_agent(agent_id)
    
    def collect_signals(self) -> Dict[str, Dict[str, Any]]:
        """
        Collect trading signals from all agents via MCP context.
        
        Returns:
            Dictionary mapping ticker symbols to latest signals from each agent
        """
        try:
            # We would normally fetch this from MCP context
            # For this demo, we'll simulate reading from a signal file
            signals_by_ticker = {}
            
            # Check if we have a signals file
            signals_file = "agent_signals.json"
            if os.path.exists(signals_file):
                try:
                    with open(signals_file, 'r') as f:
                        signals_data = json.load(f)
                    
                    # Process the signals by ticker
                    for signal in signals_data.get("signals", []):
                        ticker = signal.get("ticker")
                        if not ticker:
                            continue
                        
                        agent_type = signal.get("agent_type", "unknown")
                        
                        if ticker not in signals_by_ticker:
                            signals_by_ticker[ticker] = {}
                        
                        # Store the latest signal from each agent type
                        if (agent_type not in signals_by_ticker[ticker] or
                            signal.get("timestamp", 0) > signals_by_ticker[ticker][agent_type].get("timestamp", 0)):
                            signals_by_ticker[ticker][agent_type] = signal
                    
                except Exception as e:
                    logger.error(f"Error reading signals file: {e}")
            
            return signals_by_ticker
            
        except Exception as e:
            logger.error(f"Error collecting signals: {e}")
            return {}
    
    def make_trading_decisions(self) -> List[Dict[str, Any]]:
        """
        Make trading decisions based on collected signals.
        
        Returns:
            List of trading decisions
        """
        decisions = []
        signals_by_ticker = self.collect_signals()
        
        for ticker, signals in signals_by_ticker.items():
            # Skip if we've recently made a decision for this ticker
            if ticker in self.last_check and (datetime.now() - self.last_check[ticker]).total_seconds() < 3600:
                continue
            
            self.last_check[ticker] = datetime.now()
            
            # We need at least one signal
            if not signals:
                continue
            
            technical_signal = signals.get("technical", {})
            fundamental_signal = signals.get("fundamental", {})
            sentiment_signal = signals.get("sentiment", {})
            
            # Default to hold if we don't have a clear signal
            action = "HOLD"
            confidence = 0.5
            rationale = ["Insufficient signals for a strong decision"]
            
            # Weighted scores for each signal type
            signal_weights = {
                "technical": 0.4,    # Technical analysis for short-term signals
                "fundamental": 0.4,  # Fundamental analysis for long-term value
                "sentiment": 0.2     # Sentiment analysis for short-term sentiment shifts
            }
            
            # Calculate a combined score if we have multiple signals
            signal_scores = {
                "technical": self._calculate_signal_score(technical_signal),
                "fundamental": self._calculate_signal_score(fundamental_signal),
                "sentiment": self._calculate_signal_score(sentiment_signal)
            }
            
            # Count how many signals we have
            signal_count = sum(1 for s in signal_scores.values() if s != 0)
            
            if signal_count >= 2:  # If we have at least 2 signals
                # Calculate weighted average score
                weighted_score = 0
                total_weight = 0
                
                for signal_type, score in signal_scores.items():
                    if score != 0:  # Only consider signals we have
                        weight = signal_weights[signal_type]
                        weighted_score += score * weight
                        total_weight += weight
                
                if total_weight > 0:
                    weighted_score /= total_weight
                    
                    # Determine action based on weighted score
                    if weighted_score > 0.2:
                        action = "BUY"
                        confidence = min(0.95, (weighted_score + 0.5) / 1.5)
                    elif weighted_score < -0.2:
                        action = "SELL"
                        confidence = min(0.95, (abs(weighted_score) + 0.5) / 1.5)
                    else:
                        action = "HOLD"
                        confidence = 0.5 + (0.5 - abs(weighted_score))
                    
                    # Generate rationale
                    rationale = [f"Combined analysis of {signal_count} signals"]
                    
                    if technical_signal.get("action"):
                        rationale.append(f"Technical: {technical_signal['action']} ({technical_signal.get('confidence', 0):.2f})")
                    
                    if fundamental_signal.get("action"):
                        rationale.append(f"Fundamental: {fundamental_signal['action']} ({fundamental_signal.get('confidence', 0):.2f})")
                    
                    if sentiment_signal.get("action"):
                        rationale.append(f"Sentiment: {sentiment_signal['action']} ({sentiment_signal.get('confidence', 0):.2f})")
                    
                    # Add specific insights from each signal
                    if technical_signal.get("rationale"):
                        rationale.append(f"Tech insight: {technical_signal['rationale']}")
                    
                    if fundamental_signal.get("rationale"):
                        rationale.append(f"Fund insight: {fundamental_signal['rationale']}")
                    
                    if sentiment_signal.get("rationale"):
                        rationale.append(f"Sent insight: {sentiment_signal['rationale']}")
            
            # If we only have the technical signal
            elif technical_signal.get("action") and technical_signal.get("action") != "HOLD":
                action = technical_signal.get("action")
                confidence = min(0.75, technical_signal.get("confidence", 0.5))  # Cap at 0.75 without other signals
                
                if confidence > 0.6:
                    rationale = [
                        f"Technical analysis suggests {action}",
                        f"Technical rationale: {technical_signal.get('rationale', 'N/A')}",
                        "No fundamental or sentiment signals available for confirmation"
                    ]
                else:
                    action = "HOLD"
                    rationale = ["Technical signal not strong enough without other confirmation"]
            
            # If we only have the fundamental signal
            elif fundamental_signal.get("action") and fundamental_signal.get("action") != "HOLD":
                action = fundamental_signal.get("action")
                confidence = min(0.7, fundamental_signal.get("confidence", 0.5))  # Cap at 0.7 without other signals
                
                if confidence > 0.65:
                    rationale = [
                        f"Fundamental analysis suggests {action}",
                        f"Fundamental rationale: {fundamental_signal.get('rationale', 'N/A')}",
                        "No technical or sentiment signals available for confirmation"
                    ]
                else:
                    action = "HOLD"
                    rationale = ["Fundamental signal not strong enough without other confirmation"]
            
            # If we only have the sentiment signal
            elif sentiment_signal.get("action") and sentiment_signal.get("action") != "HOLD":
                action = sentiment_signal.get("action")
                confidence = min(0.6, sentiment_signal.get("confidence", 0.5))  # Cap at 0.6 for sentiment-only
                
                if confidence > 0.55:
                    rationale = [
                        f"Sentiment analysis suggests {action}",
                        f"Sentiment rationale: {sentiment_signal.get('rationale', 'N/A')}",
                        "No technical or fundamental signals available for confirmation"
                    ]
                else:
                    action = "HOLD"
                    rationale = ["Sentiment signal not strong enough without other confirmation"]
            
            # Create the decision
            decision = {
                "ticker": ticker,
                "action": action,
                "confidence": round(confidence, 2),
                "rationale": "; ".join(rationale),
                "timestamp": int(time.time()),
                "technical_signal": technical_signal,
                "fundamental_signal": fundamental_signal,
                "sentiment_signal": sentiment_signal
            }
            
            decisions.append(decision)
            self.decisions[ticker] = decision
            
            logger.info(f"Decision for {ticker}: {action} with confidence {confidence}")
            logger.info(f"Rationale: {'; '.join(rationale)}")
        
        return decisions
    
    def _calculate_signal_score(self, signal: Dict[str, Any]) -> float:
        """
        Calculate a normalized score for a signal (-1 to 1).
        
        Args:
            signal: Signal dictionary
            
        Returns:
            Normalized score from -1 (strong sell) to 1 (strong buy)
        """
        if not signal or "action" not in signal:
            return 0
        
        action = signal.get("action")
        confidence = signal.get("confidence", 0.5)
        
        if action == "BUY":
            return confidence - 0.5  # 0 to 0.5 range
        elif action == "SELL":
            return -1 * (confidence - 0.5)  # -0.5 to 0 range
        else:  # HOLD
            return 0
    
    def execute_decisions(self, decisions: List[Dict[str, Any]]) -> None:
        """
        Execute trading decisions.
        
        Args:
            decisions: List of trading decisions
        """
        # In a real implementation, this would connect to a trading API
        # For this demo, we'll just log the decisions
        
        for decision in decisions:
            ticker = decision.get("ticker")
            action = decision.get("action")
            confidence = decision.get("confidence")
            
            if action == "HOLD" or confidence < 0.6:
                logger.info(f"No trade executed for {ticker}: {action} with confidence {confidence}")
                continue
            
            logger.info(f"EXECUTING TRADE: {action} {ticker} with confidence {confidence}")
            logger.info(f"Rationale: {decision.get('rationale')}")
            
            # Save the decision to a file for persistence and sharing with agents
            self._save_decision(decision)
    
    def _save_decision(self, decision: Dict[str, Any]) -> None:
        """
        Save a decision to the signals file.
        
        Args:
            decision: Trading decision
        """
        signals_file = "agent_signals.json"
        
        try:
            signals_data = {"signals": []}
            
            # Load existing signals if file exists
            if os.path.exists(signals_file):
                with open(signals_file, 'r') as f:
                    signals_data = json.load(f)
            
            # Add the new decision
            decision_copy = dict(decision)
            decision_copy["agent_type"] = "orchestrator"
            signals_data["signals"].append(decision_copy)
            
            # Write back to file
            with open(signals_file, 'w') as f:
                json.dump(signals_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error saving decision: {e}")
    
    def run(self, check_interval: int = 60) -> None:
        """
        Run the orchestrator's main loop.
        
        Args:
            check_interval: Interval in seconds to check agent health and signals
        """
        logger.info("Starting Agent Orchestrator main loop")
        
        while not shutdown_requested:
            try:
                # Check agent health and restart if needed
                self.restart_unhealthy_agents()
                
                # Collect signals and make trading decisions
                decisions = self.make_trading_decisions()
                
                # Execute trading decisions
                self.execute_decisions(decisions)
                
                # Sleep until next check
                logger.debug(f"Sleeping for {check_interval} seconds...")
                for _ in range(check_interval):
                    if shutdown_requested:
                        break
                    time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in orchestrator loop: {e}")
                time.sleep(10)  # Sleep a bit before retrying

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Agent Orchestrator")
    parser.add_argument("--mcp-server", default="http://localhost:5000", 
                        help="URL of the MCP server")
    parser.add_argument("--api-key", default=None,
                        help="API key for MCP server authentication")
    parser.add_argument("--tech-agent", default="src/run_technical_agent.py",
                        help="Path to the Technical Agent script")
    parser.add_argument("--fund-agent", default="src/run_fundamental_agent.py",
                        help="Path to the Fundamental Agent script")
    parser.add_argument("--sent-agent", default="src/run_sentiment_agent.py",
                        help="Path to the Sentiment Agent script")
    parser.add_argument("--check-interval", type=int, default=60,
                        help="Interval in seconds to check agent health and signals")
    parser.add_argument("--tickers", nargs="+", 
                        default=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
                        help="List of ticker symbols to analyze")
    return parser.parse_args()

def handle_shutdown(signum, frame):
    """Handle shutdown signals."""
    global shutdown_requested
    logger.info("Shutdown requested, will exit after current operation...")
    shutdown_requested = True

def main():
    """Main execution function."""
    args = parse_args()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(
        mcp_server_url=args.mcp_server,
        api_key=args.api_key
    )
    
    # Register agents
    orchestrator.register_agent("technical", "technical", args.tech_agent)
    orchestrator.register_agent("fundamental", "fundamental", args.fund_agent)
    orchestrator.register_agent("sentiment", "sentiment", args.sent_agent)
    
    try:
        # Start agents with different intervals
        tech_args = ["--tickers"] + args.tickers + ["--interval", "300"]  # 5 minute interval for technical
        fund_args = ["--tickers"] + args.tickers + ["--interval", "3600"]  # 1 hour interval for fundamental
        sent_args = ["--tickers"] + args.tickers + ["--interval", "1800"]  # 30 minute interval for sentiment
        
        orchestrator.start_agent("technical", tech_args)
        orchestrator.start_agent("fundamental", fund_args)
        orchestrator.start_agent("sentiment", sent_args)
        
        # Run orchestrator
        orchestrator.run(args.check_interval)
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
    
    finally:
        # Stop agents
        logger.info("Stopping agents")
        orchestrator.stop_agent("technical")
        orchestrator.stop_agent("fundamental")
        orchestrator.stop_agent("sentiment")
        
        logger.info("Agent Orchestrator shutting down")
        sys.exit(0)

if __name__ == "__main__":
    main() 