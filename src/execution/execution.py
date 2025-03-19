import logging
import random
from typing import Dict, List, Any, Optional
import datetime

logger = logging.getLogger(__name__)

class ExecutionEngine:
    """
    Execution Engine that handles market order execution.
    
    This component:
    - Receives portfolio actions from the Portfolio Manager
    - Converts actions into market orders
    - Executes orders via trading API (simulated in prototype)
    - Returns execution results
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Execution Engine with configuration settings.
        
        Args:
            config: Dictionary containing configuration settings
        """
        self.config = config
        self.order_type = config['execution']['order_type']
        self.time_in_force = config['execution']['time_in_force']
        
        # Store API credentials
        self.api_key = config['api_keys']['alpaca']['api_key']
        self.api_secret = config['api_keys']['alpaca']['api_secret']
        self.api_base_url = config['api_keys']['alpaca']['base_url']
        
        # Store market data (simulated)
        self.market_prices = {}
        
        # Order history
        self.order_history = []
        
        logger.info("Initialized Execution Engine")
    
    def execute_actions(self, portfolio_actions: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Execute portfolio actions by placing orders.
        
        Args:
            portfolio_actions: Dictionary mapping symbols to portfolio actions
            
        Returns:
            Dictionary mapping symbols to execution results
        """
        execution_results = {}
        
        # Get current market prices
        self._update_market_prices(list(portfolio_actions.keys()))
        
        # Execute each action
        for symbol, action in portfolio_actions.items():
            # Skip HOLD actions
            if action['action'] == 'HOLD':
                execution_results[symbol] = {
                    'status': 'skipped',
                    'message': 'HOLD action - no order executed',
                    'timestamp': datetime.datetime.now().isoformat()
                }
                continue
            
            # Get current price
            price = self.market_prices.get(symbol)
            if not price:
                execution_results[symbol] = {
                    'status': 'error',
                    'message': f'Cannot get market price for {symbol}',
                    'timestamp': datetime.datetime.now().isoformat()
                }
                continue
            
            # Calculate quantity based on size and portfolio value
            quantity = self._calculate_quantity(action, price)
            
            # Execute the order
            result = self._place_order(symbol, action['action'], quantity, price)
            
            # Store execution result
            execution_results[symbol] = {
                'status': result['status'],
                'message': result['message'],
                'price': price,
                'quantity': quantity,
                'value': price * quantity,
                'action': action['action'],
                'timestamp': datetime.datetime.now().isoformat(),
                'order_id': result.get('order_id')
            }
            
            # Store in order history
            self.order_history.append({
                'symbol': symbol,
                'action': action['action'],
                'quantity': quantity,
                'price': price,
                'timestamp': datetime.datetime.now().isoformat(),
                'status': result['status'],
                'order_id': result.get('order_id'),
                'reason': action['reason']
            })
        
        return execution_results
    
    def _update_market_prices(self, symbols: List[str]):
        """
        Update market prices for the specified symbols.
        
        In a real implementation, this would call a market data API.
        For the prototype, we'll simulate market prices.
        
        Args:
            symbols: List of stock symbols to update
        """
        for symbol in symbols:
            # If we don't have a price yet, generate one
            if symbol not in self.market_prices:
                # Generate random price between $10 and $1000
                self.market_prices[symbol] = random.uniform(10, 1000)
            else:
                # Simulate price movement (-2% to +2%)
                price_change = self.market_prices[symbol] * random.uniform(-0.02, 0.02)
                self.market_prices[symbol] += price_change
        
        logger.debug(f"Updated market prices for {len(symbols)} symbols")
    
    def _calculate_quantity(self, action: Dict[str, Any], price: float) -> int:
        """
        Calculate the quantity of shares to trade based on the action size.
        
        Args:
            action: Portfolio action dictionary
            price: Current market price
            
        Returns:
            Quantity of shares to trade (integer)
        """
        # For the prototype, we'll assume a total portfolio value of $1M
        portfolio_value = 1000000.0  # This would be provided by the Portfolio Manager in a real implementation
        
        # Calculate target value based on size percentage
        target_value = portfolio_value * action['size']
        
        # Calculate quantity (always round down to integer)
        quantity = int(target_value / price)
        
        return max(quantity, 1)  # Ensure at least 1 share
    
    def _place_order(self, symbol: str, action_type: str, quantity: int, price: float) -> Dict[str, Any]:
        """
        Place an order for the specified symbol.
        
        In a real implementation, this would call a trading API.
        For the prototype, we'll simulate order execution.
        
        Args:
            symbol: Stock symbol
            action_type: Action type (BUY, SELL, SHORT, COVER)
            quantity: Quantity of shares
            price: Current market price
            
        Returns:
            Dictionary with order result information
        """
        # In a real implementation, this would call the Alpaca API
        # For the prototype, we'll simulate the result
        
        # Generate a random order ID
        order_id = f"order-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
        
        # 90% chance of success, 10% chance of failure
        if random.random() < 0.9:
            logger.info(f"Executed {action_type} order for {quantity} shares of {symbol} at ${price:.2f}")
            return {
                'status': 'filled',
                'message': f"Successfully executed {action_type} order for {quantity} shares at ${price:.2f}",
                'order_id': order_id
            }
        else:
            logger.warning(f"Failed to execute {action_type} order for {symbol}")
            return {
                'status': 'failed',
                'message': f"Order failed: Simulated market rejection for {symbol}",
                'order_id': None
            }
    
    def get_order_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get the order execution history.
        
        Args:
            limit: Maximum number of orders to return
            
        Returns:
            List of order history dictionaries
        """
        return self.order_history[-limit:]
    
    def get_market_price(self, symbol: str) -> Optional[float]:
        """
        Get the current market price for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Current market price or None if not available
        """
        if symbol in self.market_prices:
            return self.market_prices[symbol]
        
        # If we don't have the price, update it
        self._update_market_prices([symbol])
        return self.market_prices.get(symbol)
