"""
Order Executor module for executing market orders through external APIs.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import json
import time
import os

logger = logging.getLogger(__name__)

class OrderExecutor:
    """
    Handles execution of market orders through external APIs or simulated execution.
    Represents the Actions Layer in the trading system.
    """
    
    def __init__(self, api_key: Optional[str] = None, is_simulation: bool = True):
        """
        Initialize the Order Executor.
        
        Args:
            api_key: API key for external broker services
            is_simulation: Whether to run in simulation mode (no real trades)
        """
        self.api_key = api_key
        self.is_simulation = is_simulation
        self.executed_orders = []
        
        # Create orders directory for storing order records
        os.makedirs("orders", exist_ok=True)
        
        logger.info(f"Initializing Order Executor (simulation={is_simulation})")
    
    def execute_order(self, 
                     ticker: str, 
                     order_type: str, 
                     quantity: float, 
                     price: Optional[float] = None, 
                     time_in_force: str = "GTC",
                     order_source: str = "SYSTEM") -> Dict[str, Any]:
        """
        Execute a market or limit order.
        
        Args:
            ticker: Stock ticker symbol
            order_type: Type of order ('MARKET', 'LIMIT')
            quantity: Number of shares (positive for BUY, negative for SELL)
            price: Limit price (required for LIMIT orders)
            time_in_force: Time in force ('GTC', 'DAY', 'IOC')
            order_source: Source of the order ('SYSTEM', 'USER', 'API')
            
        Returns:
            Order execution result
        """
        logger.info(f"Executing {order_type} order for {quantity} shares of {ticker}")
        
        # Determine order action based on quantity
        action = "BUY" if quantity > 0 else "SELL"
        quantity = abs(quantity)  # Ensure quantity is positive
        
        # Generate order ID
        order_id = str(uuid.uuid4())
        
        # Create order record
        order = {
            "order_id": order_id,
            "ticker": ticker,
            "action": action,
            "order_type": order_type,
            "quantity": quantity,
            "price": price,
            "time_in_force": time_in_force,
            "status": "PENDING",
            "submitted_at": datetime.now().isoformat(),
            "executed_at": None,
            "filled_quantity": 0,
            "average_price": None,
            "source": order_source
        }
        
        if self.is_simulation:
            # Simulate order execution
            time.sleep(0.5)  # Simulate network delay
            
            # Calculate execution details (simulation)
            if order_type == "MARKET":
                # For market orders, use the current price or generate a simulated price
                execution_price = price or 100.0  # Mock price if not provided
                # Add some slippage for realism
                slippage = 0.001 * (-1 if action == "SELL" else 1)  # 0.1% slippage
                execution_price *= (1 + slippage)
            else:
                # For limit orders, use the specified price
                if not price:
                    order["status"] = "REJECTED"
                    order["rejection_reason"] = "Limit price required for LIMIT orders"
                    logger.warning(f"Limit order rejected - no price specified for {ticker}")
                    return order
                
                execution_price = price
            
            # Update order with execution details
            order["status"] = "FILLED"
            order["executed_at"] = datetime.now().isoformat()
            order["filled_quantity"] = quantity
            order["average_price"] = round(execution_price, 2)
            
            logger.info(f"Simulated {action} order for {quantity} {ticker} executed at ${execution_price:.2f}")
        
        else:
            # Real order execution through broker API would happen here
            logger.warning("Real order execution not implemented - using simulation")
            
            # For now, use simulation logic even when is_simulation=False
            time.sleep(1.0)  # Simulate longer network delay for real execution
            
            execution_price = price or 100.0
            order["status"] = "FILLED"
            order["executed_at"] = datetime.now().isoformat()
            order["filled_quantity"] = quantity
            order["average_price"] = round(execution_price, 2)
        
        # Store the executed order
        self.executed_orders.append(order)
        
        # Save order to disk
        self._save_order(order)
        
        return order
    
    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """
        Get the status of a previously submitted order.
        
        Args:
            order_id: ID of the order
            
        Returns:
            Order status and details
        """
        # Check in-memory orders first
        for order in self.executed_orders:
            if order["order_id"] == order_id:
                return order
        
        # If not found in memory, try to load from disk
        try:
            order_file = os.path.join("orders", f"{order_id}.json")
            if os.path.exists(order_file):
                with open(order_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading order {order_id}: {e}")
        
        return {"status": "NOT_FOUND", "order_id": order_id}
    
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancel a pending order.
        
        Args:
            order_id: ID of the order to cancel
            
        Returns:
            Cancellation result
        """
        order_status = self.get_order_status(order_id)
        
        if order_status["status"] == "NOT_FOUND":
            return {"status": "FAILED", "reason": "Order not found"}
        
        if order_status["status"] in ["FILLED", "CANCELLED", "REJECTED"]:
            return {"status": "FAILED", "reason": f"Cannot cancel order in {order_status['status']} state"}
        
        if self.is_simulation:
            # Simulate cancellation
            order_status["status"] = "CANCELLED"
            order_status["cancelled_at"] = datetime.now().isoformat()
            
            # Update the stored order
            self._save_order(order_status)
            
            logger.info(f"Cancelled order {order_id}")
            return {"status": "SUCCESS", "order": order_status}
        else:
            # Real cancellation through broker API would happen here
            logger.warning("Real order cancellation not implemented - using simulation")
            
            order_status["status"] = "CANCELLED"
            order_status["cancelled_at"] = datetime.now().isoformat()
            
            # Update the stored order
            self._save_order(order_status)
            
            return {"status": "SUCCESS", "order": order_status}
    
    def get_execution_history(self, ticker: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get execution history, optionally filtered by ticker.
        
        Args:
            ticker: Filter by ticker symbol
            
        Returns:
            List of executed orders
        """
        if ticker:
            return [order for order in self.executed_orders if order["ticker"] == ticker]
        else:
            return self.executed_orders
    
    def _save_order(self, order: Dict[str, Any]) -> None:
        """
        Save order to disk.
        
        Args:
            order: Order data to save
        """
        try:
            order_id = order["order_id"]
            order_file = os.path.join("orders", f"{order_id}.json")
            
            with open(order_file, 'w') as f:
                json.dump(order, f, indent=2)
                
            logger.debug(f"Saved order {order_id} to disk")
        except Exception as e:
            logger.error(f"Error saving order to disk: {e}")
    
    def create_market_buy(self, ticker: str, quantity: float) -> Dict[str, Any]:
        """
        Convenience method to create a market buy order.
        
        Args:
            ticker: Stock ticker symbol
            quantity: Number of shares to buy
            
        Returns:
            Order execution result
        """
        return self.execute_order(
            ticker=ticker,
            order_type="MARKET",
            quantity=abs(quantity),  # Ensure positive
            price=None,
            time_in_force="GTC"
        )
    
    def create_market_sell(self, ticker: str, quantity: float) -> Dict[str, Any]:
        """
        Convenience method to create a market sell order.
        
        Args:
            ticker: Stock ticker symbol
            quantity: Number of shares to sell
            
        Returns:
            Order execution result
        """
        return self.execute_order(
            ticker=ticker,
            order_type="MARKET",
            quantity=-abs(quantity),  # Ensure negative
            price=None,
            time_in_force="GTC"
        )
    
    def create_limit_buy(self, ticker: str, quantity: float, price: float) -> Dict[str, Any]:
        """
        Convenience method to create a limit buy order.
        
        Args:
            ticker: Stock ticker symbol
            quantity: Number of shares to buy
            price: Limit price
            
        Returns:
            Order execution result
        """
        return self.execute_order(
            ticker=ticker,
            order_type="LIMIT",
            quantity=abs(quantity),  # Ensure positive
            price=price,
            time_in_force="GTC"
        )
    
    def create_limit_sell(self, ticker: str, quantity: float, price: float) -> Dict[str, Any]:
        """
        Convenience method to create a limit sell order.
        
        Args:
            ticker: Stock ticker symbol
            quantity: Number of shares to sell
            price: Limit price
            
        Returns:
            Order execution result
        """
        return self.execute_order(
            ticker=ticker,
            order_type="LIMIT",
            quantity=-abs(quantity),  # Ensure negative
            price=price,
            time_in_force="GTC"
        ) 