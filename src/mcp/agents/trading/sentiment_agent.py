"""
Sentiment Analysis agent that analyzes market news and social media for trading signals.
"""
import logging
from typing import Dict, Any, Optional, List
import time

from src.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class SentimentAgent(BaseAgent):
    """Sentiment analysis agent using news and social media with MCP integration."""
    
    def __init__(self, 
                 mcp_server_url: str,
                 api_key: Optional[str] = None,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Sentiment Analysis agent.
        
        Args:
            mcp_server_url: URL of the MCP server
            api_key: Optional API key for authentication
            config: Optional configuration with parameters:
                - sentiment_thresholds: Thresholds for interpreting sentiment scores
                - source_weights: Weights for different data sources
                - lookback_periods: How far back to analyze for each source
        """
        # Set default config
        default_config = {
            "sentiment_thresholds": {
                "very_positive": 0.7,  # Score above 0.7 is very positive
                "positive": 0.55,      # Score between 0.55-0.7 is positive
                "neutral": 0.45,       # Score between 0.45-0.55 is neutral
                "negative": 0.3,       # Score between 0.3-0.45 is negative
                "very_negative": 0.0   # Score below 0.3 is very negative
            },
            "source_weights": {
                "news": 0.5,         # Weight for news articles
                "social_media": 0.3, # Weight for social media posts
                "blogs": 0.2         # Weight for financial blogs
            },
            "lookback_periods": {
                "news": 7,           # Days to look back for news
                "social_media": 3,   # Days to look back for social media
                "blogs": 14          # Days to look back for blogs
            }
        }
        
        # Merge with provided config
        merged_config = {**default_config, **(config or {})}
        
        # Initialize base class
        super().__init__("Sentiment Analysis Agent", mcp_server_url, api_key, merged_config)
        
        logger.info(f"Initialized {self.name} with source weights: {self.config['source_weights']}")
    
    def analyze(self, ticker: str) -> Dict[str, Any]:
        """
        Analyzes sentiment for a ticker symbol using news and social media data.
        
        Args:
            ticker: Ticker symbol to analyze
                
        Returns:
            Dictionary containing trading signal with confidence score
        """
        logger.info(f"{self.name} analyzing sentiment for {ticker}")
        
        # Get sentiment data using MCP tool
        sentiment_data = self._get_sentiment_data(ticker)
        
        # Get recent news using MCP tool
        news_data = self._get_news_data(ticker)
        
        # Extract overall sentiment score
        sentiment_score = sentiment_data.get("sentiment_score", 0)
        
        # Extract individual source scores
        source_scores = sentiment_data.get("source_scores", {})
        
        # Extract sentiment topics
        sentiment_topics = sentiment_data.get("topics", [])
        
        # Generate weighted sentiment score
        weighted_score = self._calculate_weighted_score(source_scores)
        
        # Analyze sentiment volume and volatility
        volume = sentiment_data.get("volume", 0)
        volatility = sentiment_data.get("volatility", 0)
        
        # Generate confidence based on volume and volatility
        confidence = self._calculate_confidence(volume, volatility)
        
        # Generate signal based on weighted sentiment score
        signal = self._generate_signal(
            ticker, 
            weighted_score, 
            confidence, 
            sentiment_topics,
            source_scores,
            news_data
        )
        
        # Share insights with other agents if signal is strong
        if signal["action"] != "HOLD" and signal["confidence"] > 0.7:
            self.send_message(
                f"Sentiment analysis indicates {signal['action']} for {ticker} with confidence {signal['confidence']}. {signal['rationale']}",
                recipients=["Technical Analysis Agent", "Fundamental Analysis Agent"]
            )
        
        return signal
    
    def _get_sentiment_data(self, ticker: str) -> Dict[str, Any]:
        """
        Get sentiment data for a ticker using MCP.
        
        Args:
            ticker: Ticker symbol
            
        Returns:
            Sentiment data
        """
        try:
            # Get sentiment analysis for each source with appropriate lookback periods
            news_days = self.config["lookback_periods"]["news"]
            
            # Call the MCP sentiment analysis tool
            result = self.call_tool("analyze_sentiment", ticker=ticker, source="all", days_back=news_days)
            
            if "error" in result:
                logger.error(f"Error getting sentiment for {ticker}: {result['error']}")
                return self._generate_mock_sentiment_data(ticker)
                
            return result
        except Exception as e:
            logger.error(f"Error getting sentiment for {ticker}: {e}")
            return self._generate_mock_sentiment_data(ticker)
    
    def _get_news_data(self, ticker: str) -> Dict[str, Any]:
        """
        Get recent news data for a ticker using MCP.
        
        Args:
            ticker: Ticker symbol
            
        Returns:
            News data
        """
        try:
            # Get news for the ticker with appropriate lookback period
            news_days = self.config["lookback_periods"]["news"]
            
            # Call the MCP news fetch tool
            result = self.call_tool("fetch_news", ticker=ticker, days_back=news_days, max_results=10)
            
            if "error" in result:
                logger.error(f"Error getting news for {ticker}: {result['error']}")
                return {"articles": []}
                
            return result
        except Exception as e:
            logger.error(f"Error getting news for {ticker}: {e}")
            return {"articles": []}
    
    def _generate_mock_sentiment_data(self, ticker: str) -> Dict[str, Any]:
        """
        Generate mock sentiment data if the MCP call fails.
        
        Args:
            ticker: Ticker symbol
            
        Returns:
            Mock sentiment data
        """
        import random
        
        # Generate a random sentiment score between 0 and 1
        sentiment_score = random.uniform(0, 1)
        
        # Determine sentiment category
        if sentiment_score >= self.config["sentiment_thresholds"]["very_positive"]:
            sentiment = "Very Positive"
        elif sentiment_score >= self.config["sentiment_thresholds"]["positive"]:
            sentiment = "Positive"
        elif sentiment_score >= self.config["sentiment_thresholds"]["neutral"]:
            sentiment = "Neutral"
        elif sentiment_score >= self.config["sentiment_thresholds"]["very_negative"]:
            sentiment = "Negative"
        else:
            sentiment = "Very Negative"
        
        # Generate source scores
        source_scores = {
            "news": random.uniform(0, 1),
            "social_media": random.uniform(0, 1),
            "blogs": random.uniform(0, 1)
        }
        
        # Generate mock topics
        possible_topics = [
            "Earnings", "Product Launch", "Management Change", 
            "Regulatory Issues", "Market Trend", "Competitor News",
            "Innovation", "Financial Health", "Partnership", "Acquisition"
        ]
        
        # Select 2-4 random topics
        num_topics = random.randint(2, 4)
        topics = random.sample(possible_topics, num_topics)
        
        # Generate mock volume and volatility
        volume = random.randint(50, 500)
        volatility = random.uniform(0.1, 0.5)
        
        return {
            "ticker": ticker,
            "sentiment_score": sentiment_score,
            "sentiment": sentiment,
            "source_scores": source_scores,
            "topics": topics,
            "volume": volume,
            "volatility": volatility
        }
    
    def _calculate_weighted_score(self, source_scores: Dict[str, float]) -> float:
        """
        Calculate weighted sentiment score from individual source scores.
        
        Args:
            source_scores: Dictionary of sentiment scores by source
            
        Returns:
            Weighted sentiment score
        """
        if not source_scores:
            return 0.5  # Neutral if no scores
        
        weighted_sum = 0
        total_weight = 0
        
        for source, score in source_scores.items():
            weight = self.config["source_weights"].get(source, 0)
            weighted_sum += score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.5  # Neutral if no weights
        
        return weighted_sum / total_weight
    
    def _calculate_confidence(self, volume: int, volatility: float) -> float:
        """
        Calculate confidence based on volume and volatility of sentiment.
        
        Args:
            volume: Volume of sentiment data
            volatility: Volatility of sentiment data
            
        Returns:
            Confidence score (0-1)
        """
        # Higher volume increases confidence
        volume_factor = min(1.0, volume / 500)  # Cap at 1.0
        
        # Higher volatility decreases confidence
        volatility_factor = max(0.0, 1.0 - volatility)
        
        # Combine factors, giving more weight to volume
        confidence = (volume_factor * 0.7) + (volatility_factor * 0.3)
        
        return max(0.1, min(0.95, confidence))  # Cap between 0.1 and 0.95
    
    def _generate_signal(self, 
                        ticker: str, 
                        sentiment_score: float, 
                        confidence: float, 
                        topics: List[str],
                        source_scores: Dict[str, float],
                        news_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate trading signal based on sentiment analysis.
        
        Args:
            ticker: Ticker symbol
            sentiment_score: Weighted sentiment score
            confidence: Confidence in the sentiment analysis
            topics: List of sentiment topics
            source_scores: Dictionary of sentiment scores by source
            news_data: Dictionary of recent news articles
            
        Returns:
            Dictionary with trading signal
        """
        # Determine action based on sentiment thresholds
        if sentiment_score >= self.config["sentiment_thresholds"]["very_positive"]:
            action = "BUY"
            rationale = f"Very positive sentiment detected for {ticker}"
        elif sentiment_score >= self.config["sentiment_thresholds"]["positive"]:
            action = "BUY"
            rationale = f"Positive sentiment detected for {ticker}"
        elif sentiment_score >= self.config["sentiment_thresholds"]["neutral"]:
            action = "HOLD"
            rationale = f"Neutral sentiment detected for {ticker}"
        elif sentiment_score >= self.config["sentiment_thresholds"]["negative"]:
            action = "SELL"
            rationale = f"Negative sentiment detected for {ticker}"
        else:
            action = "SELL"
            rationale = f"Very negative sentiment detected for {ticker}"
        
        # Include source breakdown in rationale
        source_breakdown = ", ".join([f"{source}: {score:.2f}" for source, score in source_scores.items()])
        rationale += f". Source breakdown: {source_breakdown}"
        
        # Include key topics in rationale
        if topics:
            rationale += f". Key topics: {', '.join(topics)}"
        
        # Include recent headlines if available
        recent_articles = news_data.get("articles", [])
        if recent_articles:
            # Include up to 3 most recent article titles
            headlines = [article.get("title", "") for article in recent_articles[:3]]
            headline_text = "; ".join(headlines)
            rationale += f". Recent headlines: {headline_text}"
        
        # Build the signal dictionary
        signal = {
            "ticker": ticker,
            "timestamp": time.time(),
            "action": action,
            "confidence": confidence,
            "sentiment_score": sentiment_score,
            "rationale": rationale,
            "topics": topics,
            "source_scores": source_scores
        }
        
        # Add recent headlines to the signal
        if recent_articles:
            signal["recent_headlines"] = [
                {
                    "title": article.get("title", ""),
                    "source": article.get("source", ""),
                    "url": article.get("url", ""),
                    "published_at": article.get("published_at", "")
                } 
                for article in recent_articles[:5]  # Include up to 5 headlines
            ]
        
        return signal
    
    def handle_message(self, message: Dict[str, Any]) -> None:
        """
        Handle incoming messages from other agents.
        
        Args:
            message: Message dictionary
        """
        # Example of handling a message that asks for sentiment analysis
        if message.get("type") == "request_sentiment":
            ticker = message.get("ticker")
            if ticker:
                logger.info(f"Received request for sentiment analysis of {ticker}")
                analysis = self.analyze(ticker)
                self.send_message(
                    message={
                        "type": "sentiment_response",
                        "ticker": ticker,
                        "sentiment_score": analysis["sentiment_score"],
                        "action": analysis["action"],
                        "confidence": analysis["confidence"],
                        "rationale": analysis["rationale"]
                    },
                    recipients=[message.get("sender")]
                ) 