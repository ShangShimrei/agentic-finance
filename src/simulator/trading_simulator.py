"""
Trading Simulator module for backtesting trading strategies using historical data.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import copy
import json
import os

from src.agents.agent_orchestrator import AgentOrchestrator
from src.risk_manager.risk_manager import RiskManager
from src.portfolio.portfolio_manager import PortfolioManager
from src.data_providers.market_data import MarketDataProvider

logger = logging.getLogger(__name__)

class TradingSimulator:
    """
    Trading Simulator that orchestrates agents, risk management, and portfolio management
    to simulate trading strategies using historical data.
    """
    
    def __init__(self, 
                 initial_capital: float = 100000.0,
                 risk_threshold: float = 0.5,
                 agent_configs: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize the Trading Simulator.
        
        Args:
            initial_capital: Initial capital for portfolio
            risk_threshold: Risk threshold for risk manager
            agent_configs: List of agent configurations
        """
        # Initialize components
        self.data_provider = MarketDataProvider()
        self.agent_orchestrator = AgentOrchestrator(agent_configs)
        self.risk_manager = RiskManager(risk_threshold=risk_threshold)
        self.portfolio_manager = PortfolioManager(initial_capital=initial_capital)
        
        # Simulation state
        self.current_date = None
        self.end_date = None
        self.simulation_history = []
        self.tickers = []
        
        logger.info("Initialized Trading Simulator")
    
    def configure_simulation(self, 
                            tickers: List[str],
                            start_date: datetime,
                            end_date: datetime) -> None:
        """
        Configure the simulation parameters.
        
        Args:
            tickers: List of stock tickers to trade
            start_date: Simulation start date
            end_date: Simulation end date
        """
        self.tickers = tickers
        self.current_date = start_date
        self.end_date = end_date
        self.simulation_history = []
        
        logger.info(f"Configured simulation with {len(tickers)} tickers from {start_date} to {end_date}")
    
    def _get_market_data_for_date(self, ticker: str, current_date: datetime) -> Dict[str, Any]:
        """
        Retrieve market data for a specific ticker and date.
        
        Args:
            ticker: Stock ticker
            current_date: Date to retrieve data for
            
        Returns:
            Market data for the specified date
        """
        # Start date for historical data (1 year back for calculations)
        start_date = current_date - timedelta(days=365)
        
        # Get historical prices up to current date
        historical_data = self.data_provider.get_historical_prices(ticker, start_date, current_date)
        
        # Get fundamental and sentiment data
        fundamental_data = self.data_provider.get_fundamental_data(ticker)
        news_sentiment = self.data_provider.get_news_sentiment(ticker)
        
        # Use the last available price point
        if historical_data:
            latest_data = historical_data[-1]
            current_price = latest_data["close"]
            
            # Calculate technical indicators
            ma_50 = sum(data["close"] for data in historical_data[-50:]) / min(50, len(historical_data))
            ma_200 = sum(data["close"] for data in historical_data[-200:]) / min(200, len(historical_data))
            
            # Basic RSI calculation
            gains = 0
            losses = 0
            count = min(14, len(historical_data) - 1)
            
            for i in range(len(historical_data) - count, len(historical_data)):
                change = historical_data[i]["close"] - historical_data[i-1]["close"]
                if change > 0:
                    gains += change
                else:
                    losses -= change
            
            if count > 0:
                avg_gain = gains / count
                avg_loss = losses / count
                
                if avg_loss > 0:
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))
                else:
                    rsi = 100
            else:
                rsi = 50
            
            technical_indicators = {
                "price": round(current_price, 2),
                "ma_50": round(ma_50, 2),
                "ma_200": round(ma_200, 2),
                "rsi": round(rsi, 2),
                "above_ma_50": current_price > ma_50,
                "above_ma_200": current_price > ma_200,
                "ma_50_trend": "up" if ma_50 > ma_200 else "down",
                "volume": latest_data["volume"],
                "price_change_1d": round((current_price / historical_data[-2]["close"] - 1) * 100, 2) if len(historical_data) > 1 else 0,
                "price_change_1m": round((current_price / historical_data[-min(22, len(historical_data))]["close"] - 1) * 100, 2) if len(historical_data) >= 22 else 0,
                "price_change_1y": round((current_price / historical_data[0]["close"] - 1) * 100, 2) if len(historical_data) > 0 else 0
            }
        else:
            # Fallback if no historical data
            current_price = 100.0  # Default price
            technical_indicators = {
                "price": current_price,
                "ma_50": current_price,
                "ma_200": current_price,
                "rsi": 50,
                "above_ma_50": False,
                "above_ma_200": False,
                "ma_50_trend": "neutral",
                "volume": 0,
                "price_change_1d": 0,
                "price_change_1m": 0,
                "price_change_1y": 0
            }
        
        return {
            "ticker": ticker,
            "date": current_date.strftime("%Y-%m-%d"),
            "current_price": current_price,
            "technical_indicators": technical_indicators,
            "fundamentals": fundamental_data,
            "news_sentiment": news_sentiment,
            "historical_data": historical_data[-30:] if historical_data else []  # Last 30 days
        }
    
    def run_simulation_step(self) -> Dict[str, Any]:
        """
        Run a single step of the simulation for the current date.
        
        Returns:
            Simulation step results
        """
        if self.current_date > self.end_date:
            logger.info("Simulation complete")
            return {"status": "complete"}
        
        logger.info(f"Running simulation for {self.current_date.strftime('%Y-%m-%d')}")
        
        # Results for this simulation step
        step_results = {
            "date": self.current_date.strftime("%Y-%m-%d"),
            "portfolio_before": self.portfolio_manager.get_portfolio_state(),
            "signals": [],
            "trades": [],
            "portfolio_after": None
        }
        
        # Process each ticker
        for ticker in self.tickers:
            # Get market data
            market_data = self._get_market_data_for_date(ticker, self.current_date)
            
            # Set current market price in portfolio positions
            if ticker in self.portfolio_manager.positions:
                self.portfolio_manager.positions[ticker]["last_price"] = market_data["current_price"]
            
            # Get trading signals from agents
            trading_signals = self.agent_orchestrator.analyze_market_data(market_data)
            
            # Risk-adjust the signals
            portfolio_state = self.portfolio_manager.get_portfolio_state()
            adjusted_signals = self.risk_manager.adjust_signals(trading_signals, portfolio_state)
            
            # Aggregate signals
            if adjusted_signals:
                consensus_signal = self.risk_manager.aggregate_signals(adjusted_signals)
                
                # Execute trade based on signal
                trade_result = self.portfolio_manager.process_signal(consensus_signal)
                
                # Record results
                step_results["signals"].append({
                    "ticker": ticker,
                    "raw_signals": trading_signals,
                    "adjusted_signals": adjusted_signals,
                    "consensus_signal": consensus_signal
                })
                
                step_results["trades"].append(trade_result)
        
        # Record final portfolio state
        step_results["portfolio_after"] = self.portfolio_manager.get_portfolio_state()
        
        # Add to simulation history
        self.simulation_history.append(step_results)
        
        # Move to next trading day
        self.current_date += timedelta(days=1)
        
        # Skip weekends
        while self.current_date.weekday() > 4:  # 5=Saturday, 6=Sunday
            self.current_date += timedelta(days=1)
        
        return step_results
    
    def run_complete_simulation(self) -> Dict[str, Any]:
        """
        Run the complete simulation from start to end date.
        
        Returns:
            Complete simulation results
        """
        logger.info("Starting complete simulation")
        
        while self.current_date <= self.end_date:
            self.run_simulation_step()
        
        # Calculate performance metrics
        return self.get_performance_metrics()
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Calculate performance metrics for the simulation.
        
        Returns:
            Performance metrics
        """
        if not self.simulation_history:
            return {"status": "No simulation data available"}
        
        # Initial and final portfolio values
        initial_portfolio = self.simulation_history[0]["portfolio_before"]
        final_portfolio = self.simulation_history[-1]["portfolio_after"]
        
        initial_value = initial_portfolio["total_value"]
        final_value = final_portfolio["total_value"]
        
        # Calculate returns
        absolute_return = final_value - initial_value
        percentage_return = (final_value / initial_value - 1) * 100
        
        # Get daily returns for volatility calculation
        daily_values = [step["portfolio_after"]["total_value"] for step in self.simulation_history]
        daily_returns = []
        
        for i in range(1, len(daily_values)):
            daily_return = (daily_values[i] / daily_values[i-1]) - 1
            daily_returns.append(daily_return)
        
        # Calculate volatility (standard deviation of returns)
        import numpy as np
        volatility = np.std(daily_returns) * 100 if daily_returns else 0
        
        # Count trades
        total_trades = sum(len(step["trades"]) for step in self.simulation_history)
        successful_trades = sum(
            sum(1 for trade in step["trades"] if trade.get("status") == "SUCCESS")
            for step in self.simulation_history
        )
        
        # Calculate Sharpe Ratio (simplified)
        risk_free_rate = 0.02  # Assuming 2% annual risk-free rate
        daily_risk_free = (1 + risk_free_rate) ** (1/252) - 1
        excess_returns = [r - daily_risk_free for r in daily_returns]
        sharpe_ratio = (np.mean(excess_returns) / np.std(excess_returns)) * np.sqrt(252) if excess_returns and np.std(excess_returns) > 0 else 0
        
        return {
            "simulation_period": {
                "start_date": self.simulation_history[0]["date"],
                "end_date": self.simulation_history[-1]["date"],
                "total_days": len(self.simulation_history)
            },
            "portfolio_value": {
                "initial": round(initial_value, 2),
                "final": round(final_value, 2),
                "absolute_return": round(absolute_return, 2),
                "percentage_return": round(percentage_return, 2)
            },
            "risk_metrics": {
                "volatility": round(volatility, 2),
                "sharpe_ratio": round(sharpe_ratio, 2)
            },
            "trade_metrics": {
                "total_trades": total_trades,
                "successful_trades": successful_trades,
                "success_rate": round(successful_trades / total_trades * 100 if total_trades else 0, 2)
            },
            "final_positions": final_portfolio["positions"]
        }
    
    def save_simulation_results(self, file_path: str) -> None:
        """
        Save simulation results to a file.
        
        Args:
            file_path: Path to save results
        """
        # Create results object
        results = {
            "simulation_config": {
                "tickers": self.tickers,
                "start_date": self.simulation_history[0]["date"] if self.simulation_history else None,
                "end_date": self.simulation_history[-1]["date"] if self.simulation_history else None,
                "initial_capital": self.simulation_history[0]["portfolio_before"]["total_value"] if self.simulation_history else None
            },
            "performance_metrics": self.get_performance_metrics(),
            "simulation_history": self.simulation_history
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Saved simulation results to {file_path}")
        
        return {"status": "success", "file_path": file_path} 