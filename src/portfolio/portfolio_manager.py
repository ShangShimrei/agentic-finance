"""
Portfolio Manager module that handles portfolio management and trade execution.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class PortfolioManager:
    """
    Portfolio Manager for handling trade execution and portfolio management.
    """
    
    def __init__(self, initial_capital: float = 100000.0):
        """
        Initialize the Portfolio Manager.
        
        Args:
            initial_capital: Initial capital to start with
        """
        self.cash = initial_capital
        self.positions = {}  # ticker -> {quantity, avg_price, last_price}
        self.transaction_history = []
        logger.info(f"Initializing Portfolio Manager with ${initial_capital:.2f} capital")
    
    def get_portfolio_value(self) -> float:
        """
        Calculate the total portfolio value (cash + positions).
        
        Returns:
            Total portfolio value
        """
        position_value = sum(
            pos["quantity"] * pos["last_price"] 
            for pos in self.positions.values()
        )
        
        return self.cash + position_value
    
    def get_portfolio_state(self) -> Dict[str, Any]:
        """
        Get the current portfolio state.
        
        Returns:
            Dictionary with portfolio information
        """
        portfolio_value = self.get_portfolio_value()
        
        return {
            "cash": self.cash,
            "positions": self.positions,
            "total_value": portfolio_value,
            "timestamp": datetime.now().isoformat()
        }
    
    def execute_trade(self, 
                      ticker: str, 
                      action: str, 
                      quantity: float, 
                      price: float, 
                      rationale: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a trade and update portfolio.
        
        Args:
            ticker: Stock ticker symbol
            action: 'BUY' or 'SELL'
            quantity: Number of shares to trade
            price: Price per share
            rationale: Reason for the trade
            
        Returns:
            Trade result with details
        """
        trade_value = quantity * price
        trade_result = {
            "ticker": ticker,
            "action": action,
            "quantity": quantity,
            "price": price,
            "value": trade_value,
            "timestamp": datetime.now().isoformat(),
            "status": "FAILED",
            "rationale": rationale or "N/A"
        }
        
        # Execute buy order
        if action == "BUY":
            if self.cash >= trade_value:
                # Update cash
                self.cash -= trade_value
                
                # Update position
                if ticker in self.positions:
                    # Update existing position
                    position = self.positions[ticker]
                    total_quantity = position["quantity"] + quantity
                    total_value = (position["quantity"] * position["avg_price"]) + trade_value
                    position["avg_price"] = total_value / total_quantity
                    position["quantity"] = total_quantity
                    position["last_price"] = price
                else:
                    # Create new position
                    self.positions[ticker] = {
                        "quantity": quantity,
                        "avg_price": price,
                        "last_price": price
                    }
                
                trade_result["status"] = "SUCCESS"
                logger.info(f"Bought {quantity} shares of {ticker} at ${price:.2f}")
            else:
                logger.warning(f"Insufficient funds for {ticker} purchase: need ${trade_value:.2f}, have ${self.cash:.2f}")
                trade_result["status"] = "FAILED"
                trade_result["reason"] = "Insufficient funds"
        
        # Execute sell order
        elif action == "SELL":
            if ticker in self.positions and self.positions[ticker]["quantity"] >= quantity:
                # Update cash
                self.cash += trade_value
                
                # Update position
                position = self.positions[ticker]
                position["quantity"] -= quantity
                position["last_price"] = price
                
                # Remove position if quantity becomes zero
                if position["quantity"] == 0:
                    del self.positions[ticker]
                
                trade_result["status"] = "SUCCESS"
                logger.info(f"Sold {quantity} shares of {ticker} at ${price:.2f}")
            else:
                logger.warning(f"Insufficient {ticker} shares for sale: need {quantity}, have {self.positions.get(ticker, {}).get('quantity', 0)}")
                trade_result["status"] = "FAILED"
                trade_result["reason"] = "Insufficient shares"
        
        # Record the transaction
        self.transaction_history.append(trade_result)
        
        return trade_result
    
    def process_signal(self, signal: Dict[str, Any], max_position_size: float = 0.1) -> Dict[str, Any]:
        """
        Process a trading signal and execute appropriate trades.
        
        Args:
            signal: Trading signal with action, confidence, ticker
            max_position_size: Maximum position size as a fraction of portfolio
            
        Returns:
            Trade result
        """
        ticker = signal.get("ticker")
        action = signal.get("action")
        confidence = signal.get("confidence", 0.0)
        
        if not ticker or action not in ["BUY", "SELL", "HOLD"]:
            return {"status": "FAILED", "reason": "Invalid signal format"}
        
        if action == "HOLD":
            return {"status": "SUCCESS", "action": "HOLD", "ticker": ticker}
        
        # Calculate trade size based on confidence and max position size
        portfolio_value = self.get_portfolio_value()
        max_trade_value = portfolio_value * max_position_size * confidence
        
        # Get current market price (in a real system, this would come from a market data provider)
        price = self.positions.get(ticker, {}).get("last_price", 100.0)  # Mock price
        
        # Calculate quantity based on trade value
        quantity = max_trade_value / price
        quantity = round(quantity, 2)  # Round to 2 decimal places
        
        if quantity <= 0:
            return {"status": "FAILED", "reason": "Trade size too small"}
        
        # Execute the trade
        return self.execute_trade(
            ticker=ticker,
            action=action,
            quantity=quantity,
            price=price,
            rationale=signal.get("rationale")
        ) 