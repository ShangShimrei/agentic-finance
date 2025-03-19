import logging
from typing import Dict, List, Any, Tuple
import datetime

logger = logging.getLogger(__name__)

class PortfolioManager:
    """
    Portfolio Manager that decides on portfolio actions based on risk-adjusted signals.
    
    This component:
    - Integrates risk-adjusted signals with the overall portfolio strategy
    - Determines asset allocation adjustments
    - Generates precise trading actions (Buy, Sell, Hold, etc.)
    - Maintains the current portfolio state
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Portfolio Manager with configuration settings.
        
        Args:
            config: Dictionary containing configuration settings
        """
        self.config = config
        self.max_positions = config['portfolio_manager']['max_positions']
        self.rebalance_frequency = config['portfolio_manager']['rebalance_frequency']
        self.base_currency = config['portfolio_manager']['base_currency']
        
        # Initialize portfolio state
        self.cash = 1000000.0  # Starting with $1M cash
        self.positions = {}    # Current positions {symbol: {'quantity': qty, 'value': val}}
        self.last_rebalance = None
        
        logger.info("Initialized Portfolio Manager")
    
    def determine_actions(self, risk_adjusted_signals: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Determine portfolio actions based on risk-adjusted signals.
        
        Args:
            risk_adjusted_signals: Dictionary mapping symbols to risk-adjusted signals
            
        Returns:
            Dictionary mapping symbols to portfolio actions
        """
        # Check if we should rebalance today
        if not self._should_rebalance_today():
            logger.info("Skipping rebalance based on frequency settings")
            return {}  # No actions if we're not rebalancing
        
        # Get current portfolio state
        portfolio_value = self._get_portfolio_value()
        
        # Sort symbols by confidence scores
        symbols_by_confidence = sorted(
            risk_adjusted_signals.items(),
            key=lambda x: x[1]['confidence'],
            reverse=True
        )
        
        # Determine actions for each symbol
        actions = {}
        for symbol, signal in symbols_by_confidence:
            action_type, size, reason = self._determine_action_for_symbol(symbol, signal, portfolio_value)
            
            if action_type != 'HOLD' or symbol in self.positions:  # Only include non-HOLD actions or existing positions
                actions[symbol] = {
                    'action': action_type,
                    'size': size,
                    'reason': reason,
                    'signal_confidence': signal['confidence'],
                    'signal_reasoning': signal['reasoning']
                }
        
        # Update last rebalance time
        self.last_rebalance = datetime.datetime.now()
        
        return actions
    
    def _determine_action_for_symbol(self, symbol: str, signal: Dict[str, Any], portfolio_value: float) -> Tuple[str, float, str]:
        """
        Determine the action for a specific symbol based on its signal.
        
        Args:
            symbol: The stock symbol
            signal: The risk-adjusted signal for this symbol
            portfolio_value: The current total portfolio value
            
        Returns:
            Tuple of (action_type, size, reason)
        """
        action = signal['action']
        confidence = signal['confidence']
        
        # Check if we already have a position in this symbol
        has_position = symbol in self.positions
        
        # Default values
        action_type = 'HOLD'
        size = 0.0
        reason = "No action needed"
        
        # Determine action based on the signal
        if action == 'BUY':
            if has_position:
                # Already have a position - might increase it based on confidence
                current_size = self.positions[symbol]['value'] / portfolio_value
                target_size = min(0.05 + (confidence * 0.15), 0.25)  # Max 25% position size
                
                if target_size > current_size + 0.02:  # Only buy more if increase is significant
                    action_type = 'BUY'
                    size = target_size - current_size  # Buy the difference
                    reason = f"Increasing position from {current_size:.1%} to {target_size:.1%} based on {confidence:.2f} confidence"
                else:
                    action_type = 'HOLD'
                    size = 0.0
                    reason = f"Maintaining position at {current_size:.1%}"
            else:
                # New position - size depends on confidence
                if len(self.positions) < self.max_positions:
                    action_type = 'BUY'
                    size = 0.02 + (confidence * 0.08)  # 2% to 10% position size based on confidence
                    reason = f"Opening new position at {size:.1%} based on {confidence:.2f} confidence"
                else:
                    action_type = 'HOLD'
                    size = 0.0
                    reason = f"Maximum positions ({self.max_positions}) reached, cannot open new position"
        
        elif action == 'SELL':
            if has_position:
                action_type = 'SELL'
                size = 1.0  # Sell entire position
                reason = f"Selling entire position based on sell signal with {confidence:.2f} confidence"
            else:
                if confidence > 0.7:  # Only short if very confident
                    action_type = 'SHORT'
                    size = 0.02 + (confidence * 0.05)  # 2% to 7% position size based on confidence
                    reason = f"Opening short position at {size:.1%} based on strong sell signal with {confidence:.2f} confidence"
                else:
                    action_type = 'HOLD'
                    size = 0.0
                    reason = f"Not confident enough ({confidence:.2f}) to open short position"
        
        elif action == 'HOLD':
            action_type = 'HOLD'
            size = 0.0
            if has_position:
                current_size = self.positions[symbol]['value'] / portfolio_value
                reason = f"Maintaining position at {current_size:.1%}"
            else:
                reason = "No position to maintain"
        
        return action_type, size, reason
    
    def _should_rebalance_today(self) -> bool:
        """
        Determine if we should rebalance the portfolio today based on configured frequency.
        
        Returns:
            True if we should rebalance, False otherwise
        """
        today = datetime.datetime.now()
        
        # If never rebalanced, then yes
        if self.last_rebalance is None:
            return True
        
        # Check based on rebalance frequency
        if self.rebalance_frequency == 'daily':
            # Check if the last rebalance was on a different day
            return today.date() != self.last_rebalance.date()
        
        elif self.rebalance_frequency == 'weekly':
            # Check if it's been at least 7 days since last rebalance
            delta = today - self.last_rebalance
            return delta.days >= 7
        
        elif self.rebalance_frequency == 'monthly':
            # Check if it's a different month than last rebalance
            return (today.year != self.last_rebalance.year or 
                    today.month != self.last_rebalance.month)
        
        # Default to True for unknown frequencies
        return True
    
    def _get_portfolio_value(self) -> float:
        """
        Calculate the current portfolio value (cash + positions).
        
        Returns:
            Total portfolio value
        """
        position_value = sum(pos['value'] for pos in self.positions.values())
        return self.cash + position_value
    
    def update_position(self, symbol: str, quantity: int, price: float, action: str):
        """
        Update a position in the portfolio after an execution.
        
        Args:
            symbol: The stock symbol
            quantity: The quantity of shares (positive for buy, negative for sell)
            price: The price per share
            action: The action (BUY, SELL, SHORT, COVER)
        """
        value = abs(quantity) * price
        
        if action == 'BUY':
            # Add to position
            if symbol in self.positions:
                # Update existing position
                self.positions[symbol]['quantity'] += quantity
                self.positions[symbol]['value'] += value
            else:
                # Create new position
                self.positions[symbol] = {
                    'quantity': quantity,
                    'value': value
                }
            # Deduct cash
            self.cash -= value
            
        elif action == 'SELL':
            # Reduce or close position
            if symbol in self.positions:
                self.positions[symbol]['quantity'] -= quantity
                
                # If position is closed, remove it
                if self.positions[symbol]['quantity'] <= 0:
                    del self.positions[symbol]
                else:
                    # Update value
                    self.positions[symbol]['value'] = self.positions[symbol]['quantity'] * price
                
                # Add to cash
                self.cash += value
                
        elif action == 'SHORT':
            # Add short position (negative quantity)
            if symbol in self.positions:
                # Update existing position
                self.positions[symbol]['quantity'] -= quantity  # Subtract because shorting
                self.positions[symbol]['value'] += value
            else:
                # Create new short position
                self.positions[symbol] = {
                    'quantity': -quantity,  # Negative for short
                    'value': value
                }
            # Add to cash
            self.cash += value
            
        elif action == 'COVER':
            # Cover short position
            if symbol in self.positions and self.positions[symbol]['quantity'] < 0:
                # Update position
                self.positions[symbol]['quantity'] += quantity
                
                # If position is closed, remove it
                if self.positions[symbol]['quantity'] >= 0:
                    del self.positions[symbol]
                else:
                    # Update value
                    self.positions[symbol]['value'] = abs(self.positions[symbol]['quantity']) * price
                
                # Deduct cash
                self.cash -= value
        
        # Log the update
        logger.info(f"Updated position: {symbol}, action={action}, quantity={quantity}, price=${price:.2f}")
        logger.info(f"New portfolio: cash=${self.cash:.2f}, positions={len(self.positions)}")
    
    def get_portfolio_state(self) -> Dict[str, Any]:
        """
        Get the current portfolio state.
        
        Returns:
            Dictionary with portfolio state information
        """
        position_value = sum(pos['value'] for pos in self.positions.values())
        total_value = self.cash + position_value
        
        # Calculate position sizes as percentages
        position_sizes = {}
        for symbol, position in self.positions.items():
            position_sizes[symbol] = position['value'] / total_value
        
        return {
            'cash': self.cash,
            'position_value': position_value,
            'total_value': total_value,
            'cash_percentage': self.cash / total_value,
            'positions': self.positions,
            'position_sizes': position_sizes,
            'last_rebalance': self.last_rebalance
        }
