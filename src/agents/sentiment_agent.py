import logging
import random
from typing import Dict, List, Any, Optional
import datetime
import numpy as np

logger = logging.getLogger(__name__)

class SentimentAgent:
    """
    Sentiment analysis trading agent.
    
    This agent focuses on:
    - Market sentiment analysis
    - News and social media sentiment
    - Trading volume analysis
    - Momentum indicators
    - Sentiment trends and shifts
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Sentiment Agent with configuration settings.
        
        Args:
            config: Dictionary containing configuration settings
        """
        self.config = config
        self.name = "Sentiment Analysis Agent"
        self.weight = config['agents']['sentiment']['weight']
        self.model = config['agents']['sentiment']['model']
        self.ollama_url = config['api_keys']['ollama']['base_url']
        
        # Cache for sentiment data
        self.sentiment_data = {}
        self.last_update = {}
        
        # Update frequency (30 minutes for sentiment data)
        self.update_frequency = datetime.timedelta(minutes=30)
        
        # Historical sentiment trends
        self.sentiment_history = {}
        
        logger.info(f"Initialized {self.name}")
    
    def generate_signal(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Generate trading signals for the provided symbols.
        
        Args:
            symbols: List of stock symbols to analyze
            
        Returns:
            Dictionary with symbol keys and signal dictionaries containing:
                - action: One of 'BUY', 'SELL', 'HOLD'
                - confidence: Float between 0 and 1
                - reasoning: Text explanation of decision
                - time_horizon: Investment horizon (in days)
        """
        signals = {}
        
        for symbol in symbols:
            # Get sentiment data
            sentiment = self._get_sentiment_data(symbol)
            
            if sentiment:
                # Generate signal based on sentiment analysis
                signal = self._analyze_sentiment(symbol, sentiment)
                signals[symbol] = signal
            else:
                # Fallback signal if data unavailable
                signals[symbol] = {
                    'action': 'HOLD',
                    'confidence': 0.5,
                    'reasoning': f"Insufficient sentiment data for {symbol}",
                    'time_horizon': 30  # 1 month default horizon
                }
        
        return signals
    
    def _get_sentiment_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get sentiment data for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with sentiment data or None if unavailable
        """
        now = datetime.datetime.now()
        
        # Check if we have recent data
        if (symbol in self.sentiment_data and 
            symbol in self.last_update and
            now - self.last_update[symbol] < self.update_frequency):
            return self.sentiment_data[symbol]
        
        # Get new sentiment data
        data = self._fetch_sentiment_data(symbol)
        
        if data:
            # Cache the data
            self.sentiment_data[symbol] = data
            self.last_update[symbol] = now
            
            # Update sentiment history
            if symbol not in self.sentiment_history:
                self.sentiment_history[symbol] = []
            self.sentiment_history[symbol].append(data)
            
            # Keep only last 30 days of history
            self.sentiment_history[symbol] = self.sentiment_history[symbol][-30:]
        
        return data
    
    def _fetch_sentiment_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetch sentiment data for a symbol.
        
        In a real implementation, this would:
        1. Fetch news articles and social media posts
        2. Analyze sentiment using NLP
        3. Calculate trading volume metrics
        4. Analyze price momentum
        5. Identify sentiment trends
        
        For the prototype, we generate simulated data.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with sentiment data or None if unavailable
        """
        try:
            # Generate simulated sentiment data
            now = datetime.datetime.now()
            
            # Base sentiment metrics
            news_sentiment = random.uniform(-1, 1)      # -1 to 1 scale
            social_sentiment = random.uniform(-1, 1)    # -1 to 1 scale
            volume_sentiment = random.uniform(-1, 1)    # -1 to 1 scale
            momentum_score = random.uniform(-1, 1)      # -1 to 1 scale
            
            # Generate some news headlines
            headlines = [
                {"text": f"{symbol} reports strong quarterly results", "sentiment": 0.8},
                {"text": f"Analysts upgrade {symbol} rating", "sentiment": 0.6},
                {"text": f"Market concerns over {symbol} growth", "sentiment": -0.4},
                {"text": f"New product launch from {symbol}", "sentiment": 0.5}
            ]
            random.shuffle(headlines)
            headlines = headlines[:random.randint(1, 4)]  # Take random subset
            
            # Social media metrics
            social_metrics = {
                'mentions': random.randint(100, 10000),
                'positive_ratio': random.uniform(0.3, 0.7),
                'engagement_score': random.uniform(0.1, 1.0),
                'influencer_sentiment': random.uniform(-1, 1)
            }
            
            # Volume analysis
            volume_metrics = {
                'relative_volume': random.uniform(0.5, 2.0),  # Compared to average
                'buy_volume_ratio': random.uniform(0.3, 0.7),
                'dark_pool_activity': random.uniform(0.1, 0.4),
                'options_volume_change': random.uniform(-0.5, 0.5)
            }
            
            return {
                'symbol': symbol,
                'timestamp': now.isoformat(),
                'news_sentiment': news_sentiment,
                'social_sentiment': social_sentiment,
                'volume_sentiment': volume_sentiment,
                'momentum_score': momentum_score,
                'headlines': headlines,
                'social_metrics': social_metrics,
                'volume_metrics': volume_metrics,
                'overall_sentiment': np.mean([
                    news_sentiment,
                    social_sentiment,
                    volume_sentiment,
                    momentum_score
                ])
            }
        except Exception as e:
            logger.error(f"Error fetching sentiment data for {symbol}: {e}")
            return None
    
    def _analyze_sentiment(self, symbol: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze sentiment data and generate a trading signal.
        
        Args:
            symbol: Stock symbol
            data: Sentiment data dictionary
            
        Returns:
            Signal dictionary
        """
        # Calculate component scores
        news_score = self._calculate_news_score(data)
        social_score = self._calculate_social_score(data)
        volume_score = self._calculate_volume_score(data)
        momentum_score = self._calculate_momentum_score(data)
        
        # Calculate trend score if we have history
        trend_score = self._calculate_trend_score(symbol)
        
        # Weighted sentiment score
        sentiment_score = (
            news_score * 0.3 +
            social_score * 0.2 +
            volume_score * 0.2 +
            momentum_score * 0.2 +
            (trend_score if trend_score is not None else 0.0) * 0.1
        )
        
        # Normalize to 0-1 range
        normalized_score = (sentiment_score + 1) / 2
        
        # Generate signal based on sentiment score
        if normalized_score > 0.7:  # Strong positive sentiment
            action = 'BUY'
            confidence = normalized_score
            time_horizon = 30  # 1 month
            reasoning = [
                f"Strong positive news sentiment (score: {news_score:.2f})",
                f"High social media engagement (score: {social_score:.2f})",
                f"Positive volume indicators (score: {volume_score:.2f})",
                f"Strong momentum signals (score: {momentum_score:.2f})"
            ]
            if trend_score is not None:
                reasoning.append(f"Positive sentiment trend (score: {trend_score:.2f})")
        
        elif normalized_score < 0.3:  # Strong negative sentiment
            action = 'SELL'
            confidence = 0.6 + (0.3 - normalized_score)
            time_horizon = 14  # 2 weeks
            reasoning = [
                f"Negative news sentiment (score: {news_score:.2f})",
                f"Poor social media sentiment (score: {social_score:.2f})",
                f"Concerning volume patterns (score: {volume_score:.2f})",
                f"Weak momentum signals (score: {momentum_score:.2f})"
            ]
            if trend_score is not None:
                reasoning.append(f"Negative sentiment trend (score: {trend_score:.2f})")
        
        else:  # Mixed or neutral sentiment
            action = 'HOLD'
            confidence = 0.5
            time_horizon = 7  # 1 week
            reasoning = [
                f"Mixed news sentiment (score: {news_score:.2f})",
                f"Neutral social indicators (score: {social_score:.2f})",
                f"Average trading activity (score: {volume_score:.2f})"
            ]
        
        return {
            'action': action,
            'confidence': min(confidence, 0.95),
            'reasoning': reasoning,
            'time_horizon': time_horizon,
            'analysis': {
                'sentiment_score': sentiment_score,
                'normalized_score': normalized_score,
                'news_score': news_score,
                'social_score': social_score,
                'volume_score': volume_score,
                'momentum_score': momentum_score,
                'trend_score': trend_score
            }
        }
    
    def _calculate_news_score(self, data: Dict[str, Any]) -> float:
        """Calculate news sentiment score."""
        # Combine overall news sentiment with individual headline sentiments
        headline_sentiments = [h['sentiment'] for h in data['headlines']]
        if headline_sentiments:
            avg_headline_sentiment = np.mean(headline_sentiments)
            return np.clip((data['news_sentiment'] * 0.7 + avg_headline_sentiment * 0.3), -1, 1)
        return data['news_sentiment']
    
    def _calculate_social_score(self, data: Dict[str, Any]) -> float:
        """Calculate social media sentiment score."""
        metrics = data['social_metrics']
        
        # Normalize mentions (log scale)
        normalized_mentions = min(np.log10(metrics['mentions']) / 4, 1)  # Normalize to max of 10k mentions
        
        # Combine metrics
        score = (
            data['social_sentiment'] * 0.4 +
            (metrics['positive_ratio'] * 2 - 1) * 0.2 +  # Convert to -1 to 1 scale
            metrics['engagement_score'] * 0.2 +
            metrics['influencer_sentiment'] * 0.2
        )
        
        # Weight by mention volume
        return np.clip(score * (0.7 + normalized_mentions * 0.3), -1, 1)
    
    def _calculate_volume_score(self, data: Dict[str, Any]) -> float:
        """Calculate volume analysis score."""
        metrics = data['volume_metrics']
        
        # Calculate component scores
        relative_volume_score = np.clip(metrics['relative_volume'] - 1, -1, 1)
        buy_ratio_score = (metrics['buy_volume_ratio'] * 2 - 1)  # Convert to -1 to 1 scale
        dark_pool_score = (metrics['dark_pool_activity'] * 2 - 1)
        options_score = np.clip(metrics['options_volume_change'], -1, 1)
        
        # Combine scores
        score = (
            relative_volume_score * 0.3 +
            buy_ratio_score * 0.3 +
            dark_pool_score * 0.2 +
            options_score * 0.2
        )
        
        return np.clip(score, -1, 1)
    
    def _calculate_momentum_score(self, data: Dict[str, Any]) -> float:
        """Calculate momentum score."""
        return data['momentum_score']
    
    def _calculate_trend_score(self, symbol: str) -> Optional[float]:
        """
        Calculate sentiment trend score based on historical data.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Trend score between -1 and 1, or None if insufficient history
        """
        if symbol not in self.sentiment_history or len(self.sentiment_history[symbol]) < 2:
            return None
        
        # Get recent sentiment history
        history = self.sentiment_history[symbol]
        sentiments = [h['overall_sentiment'] for h in history]
        
        # Calculate trend
        if len(sentiments) >= 7:
            # Use 7-day trend if available
            recent_avg = np.mean(sentiments[-7:])
            old_avg = np.mean(sentiments[:-7])
        else:
            # Use simple difference
            recent_avg = sentiments[-1]
            old_avg = sentiments[0]
        
        # Calculate trend score
        trend = recent_avg - old_avg
        return np.clip(trend, -1, 1)
