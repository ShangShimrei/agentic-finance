"""
Technical Analysis agent that uses technical indicators for short-term trading signals.
"""
import logging
from typing import Dict, Any, Optional, List
import time

from src.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class TechnicalAgent(BaseAgent):
    """Technical analysis agent using price action and indicators with MCP integration."""
    
    def __init__(self, 
                 mcp_server_url: str,
                 api_key: Optional[str] = None,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Technical Analysis agent.
        
        Args:
            mcp_server_url: URL of the MCP server
            api_key: Optional API key for authentication
            config: Optional configuration with parameters:
                - lookback_period: Number of periods to look back (default: 14)
                - indicators: List of indicators to use (default: ["rsi", "macd", "sma"])
                - thresholds: Custom thresholds for buy/sell signals
        """
        # Set default config
        default_config = {
            "lookback_period": 14,
            "indicators": ["rsi", "macd", "sma", "bollinger"],
            "thresholds": {
                "rsi_oversold": 30,
                "rsi_overbought": 70,
                "volume_significant": 1.5  # 1.5x average volume
            }
        }
        
        # Merge with provided config
        merged_config = {**default_config, **(config or {})}
        
        # Initialize base class
        super().__init__("Technical Analysis Agent", mcp_server_url, api_key, merged_config)
        
        logger.info(f"Initialized {self.name} with indicators: {self.config['indicators']}")
    
    def analyze(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes market data using technical analysis principles.
        
        Args:
            market_data: Dictionary containing market data including:
                - price_history: Historical price data
                - volume: Trading volume data
                - technical_indicators: Pre-calculated indicators
                
        Returns:
            Dictionary containing trading signal with confidence score
        """
        logger.info(f"{self.name} analyzing market data for {market_data.get('ticker', 'UNKNOWN')}")
        
        # Check if we should use pre-calculated indicators or calculate them ourselves
        indicators = market_data.get("technical_indicators", {})
        
        if not indicators and "price_history" in market_data:
            # We need to calculate indicators
            indicators = self._calculate_indicators(market_data)
            
            # Store the calculated indicators in context
            indicator_key = f"indicators_{market_data.get('ticker', 'UNKNOWN')}_{int(time.time())}"
            self.mcp.update_context(indicator_key, indicators)
        
        # Generate signal based on indicators
        signal = self._generate_signal(market_data, indicators)
        
        # Share insights with other agents
        if signal["action"] != "HOLD" and signal["confidence"] > 0.7:
            self.send_message(
                f"Technical analysis indicates strong {signal['action']} signal for {signal['ticker']} with confidence {signal['confidence']}. Rationale: {signal['rationale']}",
                recipients=["Fundamental Analysis Agent", "Sentiment Analysis Agent"]
            )
        
        return signal
    
    def _calculate_indicators(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate technical indicators from price history.
        
        Args:
            market_data: Market data with price history
            
        Returns:
            Dictionary of calculated indicators
        """
        # In a real implementation, this would calculate technical indicators
        # For now, we'll use the MCP to call a tool to do this
        result = self.call_tool(
            "calculate_indicators",
            ticker=market_data.get("ticker", "UNKNOWN"),
            price_data=market_data.get("price_history", []),
            volume_data=market_data.get("volume", []),
            indicators=self.config["indicators"],
            lookback_period=self.config["lookback_period"]
        )
        
        if "error" in result:
            logger.error(f"Error calculating indicators: {result['error']}")
            # Fallback to mock indicators
            return self._get_mock_indicators()
            
        return result.get("indicators", {})
    
    def _get_mock_indicators(self) -> Dict[str, Any]:
        """Generate mock indicators for prototype."""
        return {
            "rsi": 45.2,  # Neutral RSI
            "macd": {
                "macd_line": 0.2,
                "signal_line": 0.1,
                "histogram": 0.1,
                "trending_up": True
            },
            "sma": {
                "sma_20": 150.50,
                "sma_50": 145.30,
                "sma_200": 140.10,
                "price_above_sma_20": True,
                "price_above_sma_50": True,
                "price_above_sma_200": True
            },
            "bollinger": {
                "upper": 155.20,
                "middle": 150.50,
                "lower": 145.80,
                "width": 9.40,
                "percent_b": 0.55
            }
        }
    
    def _generate_signal(self, market_data: Dict[str, Any], indicators: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate trading signal based on technical indicators.
        
        Args:
            market_data: Market data
            indicators: Calculated indicators
            
        Returns:
            Trading signal
        """
        ticker = market_data.get("ticker", "UNKNOWN")
        confidence = 0.5  # Default neutral confidence
        action = "HOLD"
        rationale = []
        
        # Analyze RSI
        rsi = indicators.get("rsi")
        if rsi is not None:
            if rsi < self.config["thresholds"]["rsi_oversold"]:
                action = "BUY"
                confidence += 0.2
                rationale.append(f"RSI oversold ({rsi:.1f})")
            elif rsi > self.config["thresholds"]["rsi_overbought"]:
                action = "SELL"
                confidence += 0.2
                rationale.append(f"RSI overbought ({rsi:.1f})")
            else:
                rationale.append(f"RSI neutral ({rsi:.1f})")
        
        # Analyze MACD
        macd = indicators.get("macd", {})
        if macd:
            if macd.get("trending_up") and macd.get("histogram", 0) > 0:
                if action != "SELL":  # Don't override a SELL from RSI
                    action = "BUY"
                    confidence += 0.15
                rationale.append("MACD trending up with positive histogram")
            elif not macd.get("trending_up") and macd.get("histogram", 0) < 0:
                if action != "BUY":  # Don't override a BUY from RSI
                    action = "SELL"
                    confidence += 0.15
                rationale.append("MACD trending down with negative histogram")
            else:
                rationale.append("MACD showing mixed signals")
        
        # Analyze SMAs
        sma = indicators.get("sma", {})
        if sma:
            # Price above all SMAs is bullish
            if all([sma.get("price_above_sma_20", False), 
                    sma.get("price_above_sma_50", False),
                    sma.get("price_above_sma_200", False)]):
                if action != "SELL":  # Don't override a SELL signal
                    action = "BUY"
                    confidence += 0.1
                rationale.append("Price above all SMAs (20, 50, 200)")
            # Price below all SMAs is bearish
            elif not any([sma.get("price_above_sma_20", False), 
                         sma.get("price_above_sma_50", False),
                         sma.get("price_above_sma_200", False)]):
                if action != "BUY":  # Don't override a BUY signal
                    action = "SELL"
                    confidence += 0.1
                rationale.append("Price below all SMAs (20, 50, 200)")
            else:
                rationale.append("Mixed SMA signals")
        
        # Cap confidence at 0.95
        confidence = min(confidence, 0.95)
        
        return {
            "action": action,
            "confidence": confidence,
            "ticker": ticker,
            "rationale": "; ".join(rationale),
            "time_horizon": "SHORT",  # Technical analysis is usually short-term
            "indicators_used": list(indicators.keys())
        }
    
    def handle_message(self, message: Dict[str, Any]) -> None:
        """
        Handle an incoming message from another agent.
        
        Args:
            message: Message from another agent
        """
        super().handle_message(message)
        
        # Process messages from other agents that might influence our analysis
        sender = message.get("sender", "Unknown")
        content = message.get("message", "")
        
        # Example: If a fundamental agent warns about a company, we might adjust our strategy
        if "fundamental" in sender.lower() and "warning" in content.lower():
            logger.info(f"{self.name} received warning from {sender}, adjusting risk tolerance")
            # We could adjust thresholds or other parameters here 