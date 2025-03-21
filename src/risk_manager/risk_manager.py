"""
Risk Manager module that aggregates and risk-adjusts trading signals.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class RiskManager:
    """
    Risk Manager for aggregating and adjusting trading signals based on risk metrics.
    """
    
    def __init__(self, risk_threshold: float = 0.5):
        """
        Initialize the Risk Manager.
        
        Args:
            risk_threshold: Threshold for acceptable risk (0.0 to 1.0)
        """
        self.risk_threshold = risk_threshold
        logger.info(f"Initializing Risk Manager with risk threshold of {risk_threshold}")
    
    def calculate_var(self, portfolio: Dict[str, Any], confidence_level: float = 0.95) -> float:
        """
        Calculate Value at Risk (VaR) for the portfolio.
        
        Args:
            portfolio: Current portfolio holdings and metrics
            confidence_level: Confidence level for VaR calculation (typically 0.95 or 0.99)
            
        Returns:
            VaR value
        """
        # Placeholder implementation
        # In a real implementation, this would use historical data and statistical methods
        # to calculate VaR based on portfolio composition and historical volatility
        
        # Mock implementation returns a simple percentage of portfolio value
        portfolio_value = portfolio.get("total_value", 0)
        mock_var = portfolio_value * 0.05  # 5% VaR at the given confidence level
        
        return mock_var
    
    def adjust_signals(self, trading_signals: List[Dict[str, Any]], portfolio: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Adjust trading signals based on risk metrics.
        
        Args:
            trading_signals: List of trading signals from different agents
            portfolio: Current portfolio information
            
        Returns:
            List of risk-adjusted trading signals
        """
        logger.info(f"Adjusting {len(trading_signals)} trading signals based on risk metrics")
        
        # Calculate portfolio risk metrics
        var = self.calculate_var(portfolio)
        portfolio_value = portfolio.get("total_value", 0)
        current_risk_level = var / portfolio_value if portfolio_value else 0
        
        adjusted_signals = []
        
        for signal in trading_signals:
            # Deep copy of the original signal
            adjusted_signal = signal.copy()
            
            # Risk adjustment logic
            if current_risk_level > self.risk_threshold:
                # Higher risk environment - reduce confidence for BUY signals
                if signal["action"] == "BUY":
                    risk_factor = min(1.0, current_risk_level / self.risk_threshold)
                    adjusted_signal["confidence"] = signal["confidence"] * (1 - (risk_factor * 0.3))
                    adjusted_signal["rationale"] = f"Risk-adjusted: {signal['rationale']} (high risk environment)"
                
                # Increase confidence for SELL signals in high risk environment
                elif signal["action"] == "SELL":
                    risk_factor = min(1.0, current_risk_level / self.risk_threshold)
                    adjusted_signal["confidence"] = min(0.95, signal["confidence"] * (1 + (risk_factor * 0.2)))
                    adjusted_signal["rationale"] = f"Risk-adjusted: {signal['rationale']} (high risk environment)"
            
            adjusted_signals.append(adjusted_signal)
        
        return adjusted_signals
    
    def aggregate_signals(self, trading_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate multiple trading signals into a single consensus signal.
        
        Args:
            trading_signals: List of trading signals from different agents
            
        Returns:
            Aggregated signal representing consensus view
        """
        logger.info(f"Aggregating {len(trading_signals)} trading signals")
        
        if not trading_signals:
            return {"action": "HOLD", "confidence": 0, "rationale": "No signals available"}
        
        # Extract ticker (assuming all signals are for the same ticker)
        ticker = trading_signals[0].get("ticker", "UNKNOWN")
        
        # Count actions and calculate weighted confidence
        action_counts = {"BUY": 0, "SELL": 0, "HOLD": 0}
        action_confidences = {"BUY": 0.0, "SELL": 0.0, "HOLD": 0.0}
        agents = []
        
        for signal in trading_signals:
            action = signal["action"]
            confidence = signal["confidence"]
            
            action_counts[action] += 1
            action_confidences[action] += confidence
            agents.append(signal["agent"])
        
        # Determine consensus action (highest confidence sum)
        consensus_action = max(action_confidences, key=action_confidences.get)
        
        # Calculate aggregate confidence
        total_signals = len(trading_signals)
        consensus_count = action_counts[consensus_action]
        consensus_confidence = action_confidences[consensus_action] / total_signals
        
        # Generate rationale
        rationale = f"Consensus of {consensus_count}/{total_signals} agents: {', '.join(agents)}"
        
        return {
            "action": consensus_action,
            "confidence": consensus_confidence,
            "ticker": ticker,
            "rationale": rationale,
            "agents": agents
        } 