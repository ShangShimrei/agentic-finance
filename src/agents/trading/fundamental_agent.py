"""
Fundamental Analysis agent that evaluates financial metrics and company fundamentals.
"""
import logging
from typing import Dict, Any, Optional, List
import time

from src.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class FundamentalAgent(BaseAgent):
    """Fundamental analysis agent using financial metrics with MCP integration."""
    
    def __init__(self, 
                 mcp_server_url: str,
                 api_key: Optional[str] = None,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Fundamental Analysis agent.
        
        Args:
            mcp_server_url: URL of the MCP server
            api_key: Optional API key for authentication
            config: Optional configuration with parameters:
                - valuation_weights: Weights for different valuation metrics
                - growth_weights: Weights for growth rate metrics
                - health_weights: Weights for financial health metrics
                - market_weights: Weights for market position metrics
        """
        # Set default config
        default_config = {
            "valuation_weights": {
                "pe_ratio": 0.3,        # P/E ratio (lower is generally better)
                "price_to_book": 0.25,   # Price-to-book (lower is generally better)
                "price_to_sales": 0.2,   # Price-to-sales (lower is generally better)
                "ev_to_ebitda": 0.25     # Enterprise Value to EBITDA (lower is generally better)
            },
            "growth_weights": {
                "revenue_growth": 0.4,   # Revenue growth (higher is better)
                "earnings_growth": 0.4,  # Earnings growth (higher is better)
                "dividend_growth": 0.2   # Dividend growth (higher is better)
            },
            "health_weights": {
                "debt_to_equity": 0.4,   # Debt-to-equity ratio (lower is better)
                "current_ratio": 0.3,    # Current ratio (higher is better)
                "quick_ratio": 0.3       # Quick ratio (higher is better)
            },
            "market_weights": {
                "market_share": 0.3,          # Market share (higher is better)
                "competitive_advantage": 0.4, # Competitive advantage (higher is better)
                "industry_outlook": 0.3       # Industry outlook (higher is better)
            },
            "component_weights": {
                "valuation": 0.3,       # Overall weight for valuation metrics
                "growth": 0.3,          # Overall weight for growth metrics
                "financial_health": 0.2, # Overall weight for financial health metrics
                "market_position": 0.2   # Overall weight for market position metrics
            },
            "thresholds": {
                "buy": 0.65,            # Score above this is a buy signal
                "sell": 0.35            # Score below this is a sell signal
            }
        }
        
        # Merge with provided config
        merged_config = {**default_config, **(config or {})}
        
        # Initialize base class
        super().__init__("Fundamental Analysis Agent", mcp_server_url, api_key, merged_config)
        
        logger.info(f"Initialized {self.name} with component weights: {self.config['component_weights']}")
    
    def analyze(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes financial data for a company and generates trading signals.
        
        Args:
            financial_data: Dictionary containing financial metrics including:
                - valuation_metrics: P/E ratio, price-to-book, etc.
                - growth_rates: Revenue growth, earnings growth, etc.
                - financial_health: Debt-to-equity, current ratio, etc.
                - market_position: Market share, competitive advantage, etc.
                
        Returns:
            Dictionary containing trading signal with confidence score
        """
        ticker = financial_data.get("ticker", "UNKNOWN")
        logger.info(f"{self.name} analyzing financial data for {ticker}")
        
        # Process messages from other agents
        self.process_messages()
        
        # Calculate individual component scores
        valuation_score = self._evaluate_valuation(financial_data.get("valuation_metrics", {}))
        growth_score = self._evaluate_growth(financial_data.get("growth_rates", {}))
        health_score = self._evaluate_financial_health(financial_data.get("financial_health", {}))
        market_score = self._evaluate_market_position(financial_data.get("market_position", {}))
        
        # Create component scores dictionary
        component_scores = {
            "valuation": round(valuation_score, 2),
            "growth": round(growth_score, 2),
            "financial_health": round(health_score, 2),
            "market_position": round(market_score, 2)
        }
        
        # Calculate weighted overall score
        weights = self.config["component_weights"]
        overall_score = (
            (valuation_score * weights["valuation"]) +
            (growth_score * weights["growth"]) +
            (health_score * weights["financial_health"]) +
            (market_score * weights["market_position"])
        )
        
        # Determine action based on overall score
        thresholds = self.config["thresholds"]
        if overall_score >= thresholds["buy"]:
            action = "BUY"
            confidence = min(0.95, overall_score)
            rationale = self._generate_buy_rationale(component_scores)
        elif overall_score <= thresholds["sell"]:
            action = "SELL"
            confidence = min(0.95, 1 - overall_score)
            rationale = self._generate_sell_rationale(component_scores)
        else:
            action = "HOLD"
            # Calculate confidence based on distance from thresholds
            mid_point = (thresholds["buy"] + thresholds["sell"]) / 2
            if overall_score > mid_point:
                # Closer to buy threshold
                confidence = (overall_score - mid_point) / (thresholds["buy"] - mid_point)
            else:
                # Closer to sell threshold
                confidence = (mid_point - overall_score) / (mid_point - thresholds["sell"])
            confidence = min(0.6, confidence)  # Cap HOLD confidence at 0.6
            rationale = self._generate_hold_rationale(component_scores)
        
        # Create the signal
        signal = {
            "ticker": ticker,
            "action": action,
            "confidence": round(confidence, 2),
            "rationale": rationale,
            "overall_score": round(overall_score, 2),
            "component_scores": component_scores,
            "time_horizon": "LONG",  # Fundamental analysis is long-term focused
            "analysis_timestamp": int(time.time())
        }
        
        # Share significant insights with other agents
        if action != "HOLD" and confidence > 0.7:
            self.send_message(
                f"Fundamental analysis indicates {action} for {ticker} with confidence {confidence:.2f}. {rationale}",
                recipients=["Technical Analysis Agent", "Sentiment Analysis Agent"]
            )
        
        # Store the signal in context
        self.store_signal(signal)
        
        return signal
    
    def _evaluate_valuation(self, valuation_metrics: Dict[str, float]) -> float:
        """
        Evaluate valuation metrics and return a score (0-1).
        For valuation metrics, lower is generally better.
        
        Args:
            valuation_metrics: Dictionary of valuation metrics
            
        Returns:
            Score from 0 (poor) to 1 (excellent)
        """
        if not valuation_metrics:
            return 0.5  # Neutral if no data
        
        weights = self.config["valuation_weights"]
        total_weight = 0
        weighted_score = 0
        
        # Define target ranges for each metric
        # Format: [min_ideal, max_ideal, max_acceptable]
        metric_ranges = {
            "pe_ratio": [5, 15, 30],
            "price_to_book": [0.5, 1.5, 4],
            "price_to_sales": [0.5, 2, 5],
            "ev_to_ebitda": [4, 8, 15]
        }
        
        for metric, value in valuation_metrics.items():
            if metric not in weights:
                continue
                
            weight = weights[metric]
            
            # Calculate score for this metric
            if metric in metric_ranges:
                min_ideal, max_ideal, max_acceptable = metric_ranges[metric]
                
                if value <= min_ideal:
                    # Below ideal range (potentially undervalued)
                    metric_score = 0.9
                elif value <= max_ideal:
                    # Within ideal range
                    metric_score = 0.8
                elif value <= max_acceptable:
                    # Above ideal but still acceptable
                    normalized = (max_acceptable - value) / (max_acceptable - max_ideal)
                    metric_score = 0.5 + (normalized * 0.3)
                else:
                    # Above acceptable range
                    metric_score = max(0.1, 0.5 * (max_acceptable / value))
            else:
                # Default scoring if range not defined
                metric_score = 0.5
            
            weighted_score += metric_score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.5
            
        return weighted_score / total_weight
    
    def _evaluate_growth(self, growth_rates: Dict[str, float]) -> float:
        """
        Evaluate growth metrics and return a score (0-1).
        For growth metrics, higher is generally better.
        
        Args:
            growth_rates: Dictionary of growth rate metrics
            
        Returns:
            Score from 0 (poor) to 1 (excellent)
        """
        if not growth_rates:
            return 0.5  # Neutral if no data
        
        weights = self.config["growth_weights"]
        total_weight = 0
        weighted_score = 0
        
        # Define target ranges for each metric
        # Format: [min_acceptable, min_good, exceptional]
        metric_ranges = {
            "revenue_growth": [0.03, 0.1, 0.25],
            "earnings_growth": [0.05, 0.15, 0.3],
            "dividend_growth": [0.01, 0.05, 0.1]
        }
        
        for metric, value in growth_rates.items():
            if metric not in weights:
                continue
                
            weight = weights[metric]
            
            # Calculate score for this metric
            if metric in metric_ranges:
                min_acceptable, min_good, exceptional = metric_ranges[metric]
                
                if value < 0:
                    # Negative growth is bad
                    metric_score = max(0.1, 0.4 + (value * 2))  # -0.15 growth = 0.1, 0 growth = 0.4
                elif value < min_acceptable:
                    # Below acceptable but positive
                    metric_score = 0.4 + (value / min_acceptable) * 0.1
                elif value < min_good:
                    # Acceptable range
                    normalized = (value - min_acceptable) / (min_good - min_acceptable)
                    metric_score = 0.5 + (normalized * 0.2)
                elif value < exceptional:
                    # Good range
                    normalized = (value - min_good) / (exceptional - min_good)
                    metric_score = 0.7 + (normalized * 0.2)
                else:
                    # Exceptional range
                    metric_score = 0.9 + (0.1 * min(1, (value / exceptional) - 1))
            else:
                # Default scoring if range not defined
                metric_score = 0.5
            
            weighted_score += metric_score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.5
            
        return weighted_score / total_weight
    
    def _evaluate_financial_health(self, health_metrics: Dict[str, float]) -> float:
        """
        Evaluate financial health metrics and return a score (0-1).
        
        Args:
            health_metrics: Dictionary of financial health metrics
            
        Returns:
            Score from 0 (poor) to 1 (excellent)
        """
        if not health_metrics:
            return 0.5  # Neutral if no data
        
        weights = self.config["health_weights"]
        total_weight = 0
        weighted_score = 0
        
        # Define target ranges for each metric
        # Different metrics have different interpretations
        metric_ranges = {
            # Debt-to-equity: lower is better
            # Format: [max_ideal, max_acceptable, concerning]
            "debt_to_equity": [1.0, 2.0, 3.0],
            
            # Current ratio: higher is better
            # Format: [min_acceptable, min_good, ideal]
            "current_ratio": [1.0, 1.5, 2.0],
            
            # Quick ratio: higher is better
            # Format: [min_acceptable, min_good, ideal]
            "quick_ratio": [0.7, 1.0, 1.5]
        }
        
        for metric, value in health_metrics.items():
            if metric not in weights:
                continue
                
            weight = weights[metric]
            
            # Calculate score for this metric
            if metric == "debt_to_equity":
                max_ideal, max_acceptable, concerning = metric_ranges[metric]
                
                if value <= max_ideal:
                    # Ideal range
                    metric_score = 0.8 + (0.2 * (1 - (value / max_ideal)))
                elif value <= max_acceptable:
                    # Acceptable range
                    normalized = (max_acceptable - value) / (max_acceptable - max_ideal)
                    metric_score = 0.5 + (normalized * 0.3)
                elif value <= concerning:
                    # Concerning range
                    normalized = (concerning - value) / (concerning - max_acceptable)
                    metric_score = 0.2 + (normalized * 0.3)
                else:
                    # Above concerning threshold
                    metric_score = max(0.1, 0.2 * (concerning / value))
                    
            elif metric in ["current_ratio", "quick_ratio"]:
                min_acceptable, min_good, ideal = metric_ranges[metric]
                
                if value < min_acceptable:
                    # Below acceptable threshold
                    metric_score = max(0.1, 0.4 * (value / min_acceptable))
                elif value < min_good:
                    # Acceptable range
                    normalized = (value - min_acceptable) / (min_good - min_acceptable)
                    metric_score = 0.4 + (normalized * 0.3)
                elif value < ideal:
                    # Good range
                    normalized = (value - min_good) / (ideal - min_good)
                    metric_score = 0.7 + (normalized * 0.2)
                else:
                    # Ideal or above
                    metric_score = 0.9 + (0.1 * min(1, value / ideal - 1))
            else:
                # Default scoring if range not defined
                metric_score = 0.5
            
            weighted_score += metric_score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.5
            
        return weighted_score / total_weight
    
    def _evaluate_market_position(self, market_metrics: Dict[str, float]) -> float:
        """
        Evaluate market position metrics and return a score (0-1).
        For market position metrics, higher is generally better.
        
        Args:
            market_metrics: Dictionary of market position metrics
            
        Returns:
            Score from 0 (poor) to 1 (excellent)
        """
        if not market_metrics:
            return 0.5  # Neutral if no data
        
        weights = self.config["market_weights"]
        total_weight = 0
        weighted_score = 0
        
        # Market metrics are often rated on a 0-1 scale already, so minimal transformation needed
        for metric, value in market_metrics.items():
            if metric not in weights:
                continue
                
            weight = weights[metric]
            
            # Calculate score for this metric (assuming most metrics are already 0-1)
            if metric == "market_share":
                # Market share might be expressed as a percentage (0-1)
                if value > 0.5:  # Market dominator 
                    metric_score = 0.9 + (value - 0.5) * 0.2
                elif value > 0.2:  # Major player
                    metric_score = 0.7 + (value - 0.2) * 0.667
                elif value > 0.05:  # Significant player
                    metric_score = 0.5 + (value - 0.05) * 6.67
                elif value > 0.01:  # Minor player
                    metric_score = 0.3 + (value - 0.01) * 5
                else:  # Minimal presence
                    metric_score = value * 30
            else:
                # Most other metrics should already be on a 0-1 scale
                metric_score = value
            
            weighted_score += metric_score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.5
            
        return weighted_score / total_weight
    
    def _generate_buy_rationale(self, component_scores: Dict[str, float]) -> str:
        """
        Generate a rationale for a BUY recommendation.
        
        Args:
            component_scores: Dictionary of component scores
            
        Returns:
            Rationale string
        """
        # Find top strengths
        strengths = []
        for component, score in component_scores.items():
            if score >= 0.7:
                if component == "valuation":
                    strengths.append("attractive valuation")
                elif component == "growth":
                    strengths.append("strong growth potential")
                elif component == "financial_health":
                    strengths.append("solid financial health")
                elif component == "market_position":
                    strengths.append("strong market position")
        
        if not strengths:
            strengths.append("balanced fundamental profile")
        
        return f"BUY recommendation based on {', '.join(strengths)}. Overall fundamentals are positive."
    
    def _generate_sell_rationale(self, component_scores: Dict[str, float]) -> str:
        """
        Generate a rationale for a SELL recommendation.
        
        Args:
            component_scores: Dictionary of component scores
            
        Returns:
            Rationale string
        """
        # Find top weaknesses
        weaknesses = []
        for component, score in component_scores.items():
            if score <= 0.4:
                if component == "valuation":
                    weaknesses.append("overvaluation")
                elif component == "growth":
                    weaknesses.append("poor growth prospects")
                elif component == "financial_health":
                    weaknesses.append("concerning financial health")
                elif component == "market_position":
                    weaknesses.append("weak market position")
        
        if not weaknesses:
            weaknesses.append("deteriorating fundamental profile")
        
        return f"SELL recommendation based on {', '.join(weaknesses)}. Overall fundamentals are concerning."
    
    def _generate_hold_rationale(self, component_scores: Dict[str, float]) -> str:
        """
        Generate a rationale for a HOLD recommendation.
        
        Args:
            component_scores: Dictionary of component scores
            
        Returns:
            Rationale string
        """
        # Find strengths and weaknesses
        strengths = []
        weaknesses = []
        
        for component, score in component_scores.items():
            if score >= 0.65:
                if component == "valuation":
                    strengths.append("attractive valuation")
                elif component == "growth":
                    strengths.append("good growth potential")
                elif component == "financial_health":
                    strengths.append("solid financial health")
                elif component == "market_position":
                    strengths.append("strong market position")
            elif score <= 0.4:
                if component == "valuation":
                    weaknesses.append("concerns about valuation")
                elif component == "growth":
                    weaknesses.append("limited growth prospects")
                elif component == "financial_health":
                    weaknesses.append("financial health concerns")
                elif component == "market_position":
                    weaknesses.append("market position challenges")
        
        if strengths and weaknesses:
            return f"HOLD recommendation due to mixed signals: {', '.join(strengths)} offset by {', '.join(weaknesses)}."
        elif strengths:
            return f"HOLD recommendation with positive bias due to {', '.join(strengths)}, but waiting for better entry point."
        elif weaknesses:
            return f"HOLD recommendation with negative bias due to {', '.join(weaknesses)}, but not compelling enough to sell."
        else:
            return "HOLD recommendation based on neutral fundamental indicators."
    
    def handle_message(self, message: Dict[str, Any]) -> None:
        """
        Handle an incoming message from another agent.
        
        Args:
            message: Message from another agent
        """
        super().handle_message(message)
        
        # Process messages from other agents
        sender = message.get("sender", "Unknown")
        content = message.get("message", "")
        
        # If technical or sentiment agents send strong signals, log them
        if "Technical Analysis Agent" in sender or "Sentiment Analysis Agent" in sender:
            logger.info(f"Received message from {sender}: {content}")
            # Could use these messages to adjust our fundamental analysis focus 