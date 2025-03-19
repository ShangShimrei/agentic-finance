import logging
import numpy as np
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class RiskManager:
    """
    Risk Manager that aggregates trading signals and adjusts them based on risk metrics.
    
    This component:
    - Aggregates trading signals from all agents
    - Evaluates portfolio risk using metrics like Value-at-Risk
    - Applies position size limits and risk constraints
    - Generates risk-adjusted signals for the Portfolio Manager
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Risk Manager with configuration settings.
        
        Args:
            config: Dictionary containing configuration settings
        """
        self.config = config
        self.max_position_size = config['risk_manager']['max_position_size']
        self.max_portfolio_risk = config['risk_manager']['max_portfolio_risk']
        self.var_confidence = config['risk_manager']['value_at_risk_confidence']
        
        # Store historical portfolio values for risk calculations
        self.portfolio_history = []
        
        # Keep track of current positions and their sizes
        self.current_positions = {}
        
        logger.info("Initialized Risk Manager")
    
    def process_signals(self, agent_signals: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Process signals from all agents and adjust them based on risk metrics.
        
        Args:
            agent_signals: Dictionary mapping agent names to their signal dictionaries
            
        Returns:
            Dictionary mapping symbols to risk-adjusted signals
        """
        # First, aggregate signals by symbol
        aggregated_signals = self._aggregate_signals_by_symbol(agent_signals)
        
        # Then, apply risk constraints to each signal
        risk_adjusted_signals = self._apply_risk_constraints(aggregated_signals)
        
        return risk_adjusted_signals
    
    def _aggregate_signals_by_symbol(self, agent_signals: Dict[str, Dict[str, Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
        """
        Aggregate signals from all agents by symbol.
        
        Args:
            agent_signals: Dictionary mapping agent names to their signal dictionaries
            
        Returns:
            Dictionary mapping symbols to aggregated signals
        """
        # Initialize aggregated signals dictionary
        aggregated_signals = {}
        
        # For each agent
        for agent_name, agent_signal_dict in agent_signals.items():
            # For each symbol that this agent has a signal for
            for symbol, signal in agent_signal_dict.items():
                # If we haven't seen this symbol yet, initialize its entry
                if symbol not in aggregated_signals:
                    aggregated_signals[symbol] = {
                        'buy_confidence': 0.0,
                        'sell_confidence': 0.0,
                        'hold_confidence': 0.0,
                        'reasoning': [],
                        'agents': []
                    }
                
                # Add this agent's signal to the aggregated signal
                action = signal['action']
                confidence = signal['confidence']
                
                if action == 'BUY':
                    aggregated_signals[symbol]['buy_confidence'] += confidence
                elif action == 'SELL':
                    aggregated_signals[symbol]['sell_confidence'] += confidence
                elif action == 'HOLD':
                    aggregated_signals[symbol]['hold_confidence'] += confidence
                
                # Store the reasoning and agent name
                aggregated_signals[symbol]['reasoning'].append(f"{agent_name}: {signal['reasoning']}")
                aggregated_signals[symbol]['agents'].append(agent_name)
        
        # Normalize the confidences
        for symbol, signal in aggregated_signals.items():
            num_agents = len(signal['agents'])
            if num_agents > 0:
                signal['buy_confidence'] /= num_agents
                signal['sell_confidence'] /= num_agents
                signal['hold_confidence'] /= num_agents
            
            # Determine the final action based on the highest confidence
            confidences = {
                'BUY': signal['buy_confidence'],
                'SELL': signal['sell_confidence'],
                'HOLD': signal['hold_confidence']
            }
            signal['action'] = max(confidences, key=confidences.get)
            signal['confidence'] = confidences[signal['action']]
        
        return aggregated_signals
    
    def _apply_risk_constraints(self, aggregated_signals: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Apply risk constraints to the aggregated signals.
        
        Args:
            aggregated_signals: Dictionary mapping symbols to aggregated signals
            
        Returns:
            Dictionary mapping symbols to risk-adjusted signals
        """
        risk_adjusted_signals = {}
        
        # Calculate the overall portfolio risk
        portfolio_risk = self._calculate_portfolio_risk()
        
        # If portfolio risk exceeds the maximum allowed risk, adjust all signals
        risk_scaling_factor = 1.0
        if portfolio_risk > self.max_portfolio_risk:
            risk_scaling_factor = self.max_portfolio_risk / portfolio_risk
            logger.warning(f"Portfolio risk ({portfolio_risk:.2f}) exceeds maximum ({self.max_portfolio_risk:.2f}). "
                          f"Scaling signals by {risk_scaling_factor:.2f}")
        
        # Apply risk constraints to each signal
        for symbol, signal in aggregated_signals.items():
            # Create a copy of the signal to adjust
            adjusted_signal = signal.copy()
            
            # Adjust the confidence based on the risk scaling factor
            adjusted_signal['confidence'] *= risk_scaling_factor
            
            # Apply position size limits
            if signal['action'] == 'BUY' and (symbol in self.current_positions or 
                                              self._would_exceed_position_limit(symbol)):
                # If buying would exceed position limits, change to HOLD
                adjusted_signal['action'] = 'HOLD'
                adjusted_signal['confidence'] = max(signal['hold_confidence'], 0.5)
                adjusted_signal['reasoning'].append(
                    f"Risk Manager: Position size would exceed limit of {self.max_position_size*100:.0f}%")
            
            # Add risk assessment to the reasoning
            adjusted_signal['reasoning'].append(
                f"Risk Manager: Portfolio risk at {portfolio_risk:.2f}, scaling factor {risk_scaling_factor:.2f}")
            
            # Store the adjusted signal
            risk_adjusted_signals[symbol] = adjusted_signal
        
        return risk_adjusted_signals
    
    def _calculate_portfolio_risk(self) -> float:
        """
        Calculate the overall portfolio risk using Value-at-Risk.
        
        For the prototype, this is a simplified calculation.
        In a real implementation, this would use historical returns and proper VaR calculations.
        
        Returns:
            Portfolio risk as a number between 0 and 1
        """
        # If we don't have enough history, return a default value
        if len(self.portfolio_history) < 30:
            return 0.1  # Default risk value
        
        # Calculate daily returns
        returns = np.diff(self.portfolio_history) / self.portfolio_history[:-1]
        
        # Calculate Value-at-Risk
        var = -np.percentile(returns, 100 * (1 - self.var_confidence))
        
        # Normalize to a value between 0 and 1
        normalized_risk = min(var * 10, 1.0)  # Scale VaR to a 0-1 range
        
        return normalized_risk
    
    def _would_exceed_position_limit(self, symbol: str) -> bool:
        """
        Check if buying a symbol would exceed the maximum position size.
        
        Args:
            symbol: The symbol to check
            
        Returns:
            True if buying would exceed position limits, False otherwise
        """
        # For the prototype, we'll assume equal position sizes
        # In a real implementation, this would consider actual position sizes and cash available
        num_positions = len(self.current_positions)
        if num_positions >= self.config['portfolio_manager']['max_positions']:
            return True
        
        # Check if adding this position would exceed the max position size
        if symbol not in self.current_positions:
            new_position_size = 1.0 / (num_positions + 1)
            return new_position_size > self.max_position_size
        
        return False
    
    def update_portfolio_state(self, portfolio_value: float, positions: Dict[str, float]):
        """
        Update the risk manager's state with the current portfolio value and positions.
        
        Args:
            portfolio_value: The current total portfolio value
            positions: Dictionary mapping symbols to position sizes (as percentage of portfolio)
        """
        self.portfolio_history.append(portfolio_value)
        self.current_positions = positions
        
        # Keep only the last 100 days of history
        if len(self.portfolio_history) > 100:
            self.portfolio_history = self.portfolio_history[-100:]
