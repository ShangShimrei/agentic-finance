import logging
import random
from typing import Dict, List, Any, Optional
import datetime
import numpy as np

logger = logging.getLogger(__name__)

class TechnicalAgent:
    """
    Technical analysis trading agent.
    
    This agent focuses on:
    - Price action and patterns
    - Technical indicators
    - Chart patterns
    - Support and resistance levels
    - Volume analysis
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Technical Agent with configuration settings.
        
        Args:
            config: Dictionary containing configuration settings
        """
        self.config = config
        self.name = "Technical Analysis Agent"
        self.weight = config['agents']['technical']['weight']
        
        # Cache for technical data
        self.technical_data = {}
        self.last_update = {}
        
        # Update frequency (5 minutes for technical data)
        self.update_frequency = datetime.timedelta(minutes=5)
        
        # Price history for pattern recognition
        self.price_history = {}
        
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
            # Get technical data
            data = self._get_technical_data(symbol)
            
            if data:
                # Generate signal based on technical analysis
                signal = self._analyze_technicals(symbol, data)
                signals[symbol] = signal
            else:
                # Fallback signal if data unavailable
                signals[symbol] = {
                    'action': 'HOLD',
                    'confidence': 0.5,
                    'reasoning': f"Insufficient technical data for {symbol}",
                    'time_horizon': 5  # 5 days default horizon
                }
        
        return signals
    
    def _get_technical_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get technical data for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with technical data or None if unavailable
        """
        now = datetime.datetime.now()
        
        # Check if we have recent data
        if (symbol in self.technical_data and 
            symbol in self.last_update and
            now - self.last_update[symbol] < self.update_frequency):
            return self.technical_data[symbol]
        
        # Get new technical data
        data = self._fetch_technical_data(symbol)
        
        if data:
            # Cache the data
            self.technical_data[symbol] = data
            self.last_update[symbol] = now
            
            # Update price history
            if symbol not in self.price_history:
                self.price_history[symbol] = []
            self.price_history[symbol].append({
                'timestamp': now,
                'price': data['price'],
                'volume': data['volume']
            })
            
            # Keep only last 100 price points
            self.price_history[symbol] = self.price_history[symbol][-100:]
        
        return data
    
    def _fetch_technical_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetch technical data for a symbol.
        
        In a real implementation, this would:
        1. Fetch price and volume data
        2. Calculate technical indicators
        3. Identify chart patterns
        4. Calculate support/resistance levels
        
        For the prototype, we generate simulated data.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with technical data or None if unavailable
        """
        try:
            now = datetime.datetime.now()
            
            # Generate base price and volume
            price = random.uniform(10, 1000)
            volume = random.randint(100000, 10000000)
            
            # Technical indicators
            rsi = random.uniform(0, 100)
            macd = random.uniform(-2, 2)
            macd_signal = random.uniform(-2, 2)
            macd_histogram = macd - macd_signal
            
            # Moving averages
            ma_20 = price * random.uniform(0.95, 1.05)
            ma_50 = price * random.uniform(0.90, 1.10)
            ma_200 = price * random.uniform(0.85, 1.15)
            
            # Bollinger Bands
            bb_middle = price
            bb_upper = price * 1.05
            bb_lower = price * 0.95
            
            # Support and resistance
            support_levels = [
                price * 0.95,
                price * 0.90,
                price * 0.85
            ]
            resistance_levels = [
                price * 1.05,
                price * 1.10,
                price * 1.15
            ]
            
            # Patterns
            patterns = []
            pattern_types = ['Double Bottom', 'Head and Shoulders', 'Triangle', 'Flag', 'Channel']
            if random.random() < 0.3:  # 30% chance of pattern
                patterns.append({
                    'type': random.choice(pattern_types),
                    'confidence': random.uniform(0.6, 0.9),
                    'target': price * random.uniform(0.9, 1.1)
                })
            
            return {
                'symbol': symbol,
                'timestamp': now.isoformat(),
                'price': price,
                'volume': volume,
                'indicators': {
                    'rsi': rsi,
                    'macd': macd,
                    'macd_signal': macd_signal,
                    'macd_histogram': macd_histogram,
                    'ma_20': ma_20,
                    'ma_50': ma_50,
                    'ma_200': ma_200,
                    'bb_upper': bb_upper,
                    'bb_middle': bb_middle,
                    'bb_lower': bb_lower
                },
                'support_levels': support_levels,
                'resistance_levels': resistance_levels,
                'patterns': patterns,
                'trend': {
                    'short_term': random.choice(['up', 'down', 'sideways']),
                    'medium_term': random.choice(['up', 'down', 'sideways']),
                    'long_term': random.choice(['up', 'down', 'sideways'])
                }
            }
        except Exception as e:
            logger.error(f"Error fetching technical data for {symbol}: {e}")
            return None
    
    def _analyze_technicals(self, symbol: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze technical data and generate a trading signal.
        
        Args:
            symbol: Stock symbol
            data: Technical data dictionary
            
        Returns:
            Signal dictionary
        """
        # Calculate component scores
        trend_score = self._calculate_trend_score(data)
        momentum_score = self._calculate_momentum_score(data)
        pattern_score = self._calculate_pattern_score(data)
        support_resistance_score = self._calculate_support_resistance_score(data)
        volume_score = self._calculate_volume_score(symbol, data)
        
        # Calculate weighted technical score
        technical_score = (
            trend_score * 0.3 +
            momentum_score * 0.25 +
            pattern_score * 0.2 +
            support_resistance_score * 0.15 +
            volume_score * 0.1
        )
        
        # Generate signal based on technical score
        if technical_score > 0.7:  # Strong bullish signals
            action = 'BUY'
            confidence = technical_score
            time_horizon = 5  # 5 days
            reasoning = [
                f"Strong trend signals (score: {trend_score:.2f})",
                f"Positive momentum indicators (score: {momentum_score:.2f})",
                f"Bullish chart patterns (score: {pattern_score:.2f})",
                f"Price near support levels (score: {support_resistance_score:.2f})"
            ]
        
        elif technical_score < 0.3:  # Strong bearish signals
            action = 'SELL'
            confidence = 0.6 + (0.3 - technical_score)
            time_horizon = 5  # 5 days
            reasoning = [
                f"Weak trend signals (score: {trend_score:.2f})",
                f"Negative momentum indicators (score: {momentum_score:.2f})",
                f"Bearish chart patterns (score: {pattern_score:.2f})",
                f"Price near resistance levels (score: {support_resistance_score:.2f})"
            ]
        
        else:  # Mixed signals
            action = 'HOLD'
            confidence = 0.5
            time_horizon = 3  # 3 days
            reasoning = [
                f"Mixed trend signals (score: {trend_score:.2f})",
                f"Neutral momentum (score: {momentum_score:.2f})",
                f"No clear chart patterns (score: {pattern_score:.2f})"
            ]
        
        return {
            'action': action,
            'confidence': min(confidence, 0.95),
            'reasoning': reasoning,
            'time_horizon': time_horizon,
            'analysis': {
                'technical_score': technical_score,
                'trend_score': trend_score,
                'momentum_score': momentum_score,
                'pattern_score': pattern_score,
                'support_resistance_score': support_resistance_score,
                'volume_score': volume_score
            }
        }
    
    def _calculate_trend_score(self, data: Dict[str, Any]) -> float:
        """Calculate trend score based on moving averages and trends."""
        price = data['price']
        indicators = data['indicators']
        
        # Moving average relationships
        ma_scores = [
            1 if price > indicators['ma_20'] else -1,
            1 if price > indicators['ma_50'] else -1,
            1 if price > indicators['ma_200'] else -1,
            1 if indicators['ma_20'] > indicators['ma_50'] else -1,
            1 if indicators['ma_50'] > indicators['ma_200'] else -1
        ]
        
        # Trend directions
        trend_scores = {
            'up': 1,
            'sideways': 0,
            'down': -1
        }
        trend_weights = {
            'short_term': 0.5,
            'medium_term': 0.3,
            'long_term': 0.2
        }
        
        trend_score = sum(
            trend_scores[data['trend'][term]] * weight
            for term, weight in trend_weights.items()
        )
        
        # Combine scores
        ma_score = np.mean(ma_scores)
        final_score = (ma_score * 0.6 + trend_score * 0.4)
        
        return (final_score + 1) / 2  # Normalize to 0-1
    
    def _calculate_momentum_score(self, data: Dict[str, Any]) -> float:
        """Calculate momentum score based on technical indicators."""
        indicators = data['indicators']
        
        # RSI score (normalized from 0-100 to 0-1)
        rsi = indicators['rsi']
        if rsi > 70:
            rsi_score = (100 - rsi) / 30  # Overbought
        elif rsi < 30:
            rsi_score = rsi / 30  # Oversold
        else:
            rsi_score = 0.5 + (rsi - 50) / 40
        
        # MACD score
        macd_score = 0.5
        if indicators['macd_histogram'] > 0:
            macd_score += min(indicators['macd_histogram'], 1) * 0.5
        else:
            macd_score -= min(abs(indicators['macd_histogram']), 1) * 0.5
        
        # Bollinger Bands position
        bb_score = 0.5
        price = data['price']
        if price > indicators['bb_upper']:
            bb_score = 0.2  # Overbought
        elif price < indicators['bb_lower']:
            bb_score = 0.8  # Oversold
        else:
            # Normalize position within bands
            bb_range = indicators['bb_upper'] - indicators['bb_lower']
            if bb_range > 0:
                position = (price - indicators['bb_lower']) / bb_range
                bb_score = position
        
        # Combine scores
        return np.clip(rsi_score * 0.4 + macd_score * 0.4 + bb_score * 0.2, 0, 1)
    
    def _calculate_pattern_score(self, data: Dict[str, Any]) -> float:
        """Calculate pattern score based on identified chart patterns."""
        if not data['patterns']:
            return 0.5  # Neutral if no patterns
        
        # Calculate weighted score based on pattern confidence
        pattern_scores = []
        for pattern in data['patterns']:
            # Determine if pattern is bullish or bearish
            is_bullish = pattern['target'] > data['price']
            score = pattern['confidence'] if is_bullish else (1 - pattern['confidence'])
            pattern_scores.append(score)
        
        return np.mean(pattern_scores)
    
    def _calculate_support_resistance_score(self, data: Dict[str, Any]) -> float:
        """Calculate score based on proximity to support/resistance levels."""
        price = data['price']
        
        # Find closest support and resistance
        closest_support = min(
            (abs(price - level), level) 
            for level in data['support_levels']
        )[1]
        
        closest_resistance = min(
            (abs(price - level), level)
            for level in data['resistance_levels']
        )[1]
        
        # Calculate distances as percentages
        support_distance = (price - closest_support) / price
        resistance_distance = (closest_resistance - price) / price
        
        # Score based on relative position
        if support_distance < resistance_distance:
            # Closer to support (bullish)
            score = 0.5 + (0.5 * (1 - support_distance / resistance_distance))
        else:
            # Closer to resistance (bearish)
            score = 0.5 * (support_distance / resistance_distance)
        
        return np.clip(score, 0, 1)
    
    def _calculate_volume_score(self, symbol: str, data: Dict[str, Any]) -> float:
        """Calculate volume analysis score."""
        if symbol not in self.price_history or len(self.price_history[symbol]) < 2:
            return 0.5  # Neutral if insufficient history
        
        # Get recent volume history
        history = self.price_history[symbol]
        volumes = [h['volume'] for h in history]
        
        # Calculate average volume
        avg_volume = np.mean(volumes[:-1])  # Exclude current volume
        
        # Score based on relative volume
        relative_volume = data['volume'] / avg_volume if avg_volume > 0 else 1.0
        
        # Normalize score (1.5x volume = score of 0.75, 0.5x volume = score of 0.25)
        volume_score = 0.5 + (np.clip(np.log2(relative_volume), -1, 1) * 0.25)
        
        return volume_score
