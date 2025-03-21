"""
Tools for the Model Context Protocol (MCP) Server.

This module contains tool functions that agents can call via the MCP server.
"""
import logging
import time
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

def calculate_indicators(ticker: str, 
                        price_data: List[float], 
                        volume_data: Optional[List[float]] = None, 
                        indicators: Optional[List[str]] = None,
                        lookback_period: int = 14) -> Dict[str, Any]:
    """
    Calculate technical indicators from price history.
    
    Args:
        ticker: Ticker symbol
        price_data: List of historical prices
        volume_data: Optional list of volume data
        indicators: List of indicators to calculate
        lookback_period: Number of periods to look back
        
    Returns:
        Dictionary of calculated indicators
    """
    logger.info(f"Calculating indicators for {ticker}")
    
    if not indicators:
        indicators = ["rsi", "macd", "sma", "bollinger"]
    
    if not price_data or len(price_data) < lookback_period:
        logger.warning(f"Insufficient price data for {ticker}, using mock data")
        return _get_mock_indicators(ticker)
    
    result = {}
    
    # Convert to pandas Series for easier calculation
    prices = pd.Series(price_data)
    
    # Calculate RSI if requested
    if "rsi" in indicators:
        result["rsi"] = _calculate_rsi(prices, lookback_period)
    
    # Calculate MACD if requested
    if "macd" in indicators:
        result["macd"] = _calculate_macd(prices)
    
    # Calculate SMAs if requested
    if "sma" in indicators:
        result["sma"] = _calculate_sma(prices)
    
    # Calculate Bollinger Bands if requested
    if "bollinger" in indicators:
        result["bollinger"] = _calculate_bollinger_bands(prices)
    
    # Add custom analysis
    if "price_volume" in indicators and volume_data:
        volumes = pd.Series(volume_data)
        result["price_volume"] = _analyze_price_volume(prices, volumes)
    
    return {
        "ticker": ticker,
        "indicators": result,
        "timestamp": time.time(),
        "data_points": len(price_data)
    }

def fetch_market_data(ticker: str, period: str = "1d", lookback: int = 30) -> Dict[str, Any]:
    """
    Fetch market data for a ticker.
    This is a mock implementation that would normally call a market data API.
    
    Args:
        ticker: Ticker symbol
        period: Data period ("1d", "1h", etc.)
        lookback: Number of periods to look back
        
    Returns:
        Market data including price history and volume
    """
    logger.info(f"Fetching market data for {ticker}, period={period}, lookback={lookback}")
    
    # Mock implementation that generates synthetic data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=lookback)
    
    # Generate date range
    date_range = pd.date_range(start=start_date, end=end_date, periods=lookback)
    
    # Generate mock price data with trend and some random noise
    base_price = 100 + random.random() * 900  # Random base price between 100 and 1000
    trend = random.choice([-1, 1]) * random.random() * 0.1  # Random trend direction and magnitude
    
    price_data = []
    for i in range(lookback):
        noise = random.random() * 2 - 1  # Random noise between -1 and 1
        price = base_price * (1 + trend * i / lookback + noise * 0.01)
        price_data.append(round(price, 2))
    
    # Generate mock volume data
    volume_data = [int(random.random() * 1000000 + 100000) for _ in range(lookback)]
    
    # Create OHLC data
    ohlc_data = []
    for i, price in enumerate(price_data):
        if i > 0:
            prev_price = price_data[i-1]
        else:
            prev_price = price
        
        open_price = prev_price
        close_price = price
        high_price = max(open_price, close_price) * (1 + random.random() * 0.01)
        low_price = min(open_price, close_price) * (1 - random.random() * 0.01)
        
        ohlc_data.append({
            "date": date_range[i].strftime("%Y-%m-%d"),
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": volume_data[i]
        })
    
    return {
        "ticker": ticker,
        "period": period,
        "data": ohlc_data,
        "price_history": price_data,
        "volume": volume_data,
        "timestamp": time.time()
    }

def analyze_sentiment(ticker: str, source: str = "all") -> Dict[str, Any]:
    """
    Analyze market sentiment for a ticker.
    This is a mock implementation that would normally call a sentiment analysis service.
    
    Args:
        ticker: Ticker symbol
        source: Source of sentiment data ("twitter", "news", "reddit", "all")
        
    Returns:
        Sentiment analysis results
    """
    logger.info(f"Analyzing sentiment for {ticker} from {source}")
    
    # Mock sentiment analysis results
    sentiment_score = random.random() * 2 - 1  # Between -1 and 1
    
    # Generate different scores for different sources
    source_scores = {}
    if source == "all" or source == "twitter":
        source_scores["twitter"] = sentiment_score * (0.8 + random.random() * 0.4)
    if source == "all" or source == "news":
        source_scores["news"] = sentiment_score * (0.7 + random.random() * 0.6)
    if source == "all" or source == "reddit":
        source_scores["reddit"] = sentiment_score * (0.6 + random.random() * 0.8)
    
    # Generate mock sentiment topics
    topics = []
    if sentiment_score > 0.3:
        topics = ["growth", "innovation", "earnings", "expansion"]
    elif sentiment_score < -0.3:
        topics = ["risk", "competition", "expenses", "regulation"]
    else:
        topics = ["neutral", "mixed", "steady", "stable"]
    
    # Randomly select 2-3 topics
    selected_topics = random.sample(topics, min(len(topics), random.randint(2, 3)))
    
    return {
        "ticker": ticker,
        "sentiment_score": round(sentiment_score, 2),
        "source_scores": {k: round(v, 2) for k, v in source_scores.items()},
        "topics": selected_topics,
        "volume": random.randint(100, 10000),
        "sentiment": _score_to_sentiment(sentiment_score),
        "timestamp": time.time()
    }

def generate_trade_recommendation(ticker: str, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a trade recommendation based on multiple signals.
    
    Args:
        ticker: Ticker symbol
        signals: List of trading signals from different agents
        
    Returns:
        Trade recommendation
    """
    logger.info(f"Generating trade recommendation for {ticker} from {len(signals)} signals")
    
    if not signals:
        return {
            "ticker": ticker,
            "recommendation": "HOLD",
            "confidence": 0.5,
            "timestamp": time.time(),
            "note": "No signals provided"
        }
    
    # Count the number of each action type
    action_counts = {"BUY": 0, "SELL": 0, "HOLD": 0}
    weighted_confidence = {"BUY": 0.0, "SELL": 0.0, "HOLD": 0.0}
    total_weights = 0.0
    
    for signal in signals:
        action = signal.get("action", "HOLD")
        confidence = signal.get("confidence", 0.5)
        weight = signal.get("weight", 1.0)
        
        action_counts[action] += 1
        weighted_confidence[action] += confidence * weight
        total_weights += weight
    
    # Determine the recommended action
    if total_weights > 0:
        for action in weighted_confidence:
            weighted_confidence[action] /= total_weights
    
    # Find the action with the highest weighted confidence
    recommended_action = max(weighted_confidence, key=weighted_confidence.get)
    confidence = weighted_confidence[recommended_action]
    
    # Generate a rationale
    if recommended_action == "BUY":
        rationale = f"{action_counts['BUY']} out of {len(signals)} signals suggest buying"
    elif recommended_action == "SELL":
        rationale = f"{action_counts['SELL']} out of {len(signals)} signals suggest selling"
    else:
        rationale = f"Mixed signals with no clear direction"
    
    return {
        "ticker": ticker,
        "recommendation": recommended_action,
        "confidence": round(confidence, 2),
        "rationale": rationale,
        "signal_breakdown": action_counts,
        "timestamp": time.time()
    }

# Helper functions

def _calculate_rsi(prices: pd.Series, period: int = 14) -> float:
    """Calculate RSI indicator."""
    # This is a simplified implementation of RSI
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    
    try:
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return float(rsi.iloc[-1])
    except:
        # Return a value in the middle if calculation fails
        return 50.0

def _calculate_macd(prices: pd.Series) -> Dict[str, Any]:
    """Calculate MACD indicator."""
    # This is a simplified implementation of MACD
    ema12 = prices.ewm(span=12, adjust=False).mean()
    ema26 = prices.ewm(span=26, adjust=False).mean()
    
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line
    
    trending_up = macd_line.iloc[-1] > signal_line.iloc[-1]
    
    return {
        "macd_line": float(macd_line.iloc[-1]),
        "signal_line": float(signal_line.iloc[-1]),
        "histogram": float(histogram.iloc[-1]),
        "trending_up": trending_up
    }

def _calculate_sma(prices: pd.Series) -> Dict[str, Any]:
    """Calculate SMA indicator."""
    sma20 = prices.rolling(window=20).mean()
    sma50 = prices.rolling(window=50).mean()
    sma200 = prices.rolling(window=200).mean()
    
    latest_price = prices.iloc[-1]
    
    return {
        "sma_20": float(sma20.iloc[-1]) if not pd.isna(sma20.iloc[-1]) else float(latest_price),
        "sma_50": float(sma50.iloc[-1]) if not pd.isna(sma50.iloc[-1]) else float(latest_price),
        "sma_200": float(sma200.iloc[-1]) if not pd.isna(sma200.iloc[-1]) else float(latest_price),
        "price_above_sma_20": latest_price > sma20.iloc[-1] if not pd.isna(sma20.iloc[-1]) else True,
        "price_above_sma_50": latest_price > sma50.iloc[-1] if not pd.isna(sma50.iloc[-1]) else True,
        "price_above_sma_200": latest_price > sma200.iloc[-1] if not pd.isna(sma200.iloc[-1]) else True
    }

def _calculate_bollinger_bands(prices: pd.Series, window: int = 20, num_std: int = 2) -> Dict[str, Any]:
    """Calculate Bollinger Bands."""
    sma = prices.rolling(window=window).mean()
    std = prices.rolling(window=window).std()
    
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    
    latest_price = prices.iloc[-1]
    latest_sma = float(sma.iloc[-1]) if not pd.isna(sma.iloc[-1]) else float(latest_price)
    latest_upper = float(upper_band.iloc[-1]) if not pd.isna(upper_band.iloc[-1]) else float(latest_price * 1.1)
    latest_lower = float(lower_band.iloc[-1]) if not pd.isna(lower_band.iloc[-1]) else float(latest_price * 0.9)
    
    # Calculate %B
    try:
        percent_b = (latest_price - latest_lower) / (latest_upper - latest_lower)
    except ZeroDivisionError:
        percent_b = 0.5
    
    return {
        "upper": latest_upper,
        "middle": latest_sma,
        "lower": latest_lower,
        "width": latest_upper - latest_lower,
        "percent_b": percent_b
    }

def _analyze_price_volume(prices: pd.Series, volumes: pd.Series) -> Dict[str, Any]:
    """Analyze price and volume relationship."""
    price_change = prices.pct_change()
    volume_change = volumes.pct_change()
    
    # Identify high volume days
    avg_volume = volumes.mean()
    high_volume = volumes > (avg_volume * 1.5)
    
    # Identify price-volume divergence
    price_up_volume_down = (price_change > 0) & (volume_change < 0)
    price_down_volume_up = (price_change < 0) & (volume_change > 0)
    
    return {
        "high_volume_days": int(high_volume.sum()),
        "price_up_volume_down": int(price_up_volume_down.sum()),
        "price_down_volume_up": int(price_down_volume_up.sum()),
        "avg_volume": float(avg_volume),
        "latest_volume": float(volumes.iloc[-1]),
        "volume_ratio": float(volumes.iloc[-1] / avg_volume)
    }

def _get_mock_indicators(ticker: str) -> Dict[str, Any]:
    """Generate mock indicators for prototype."""
    return {
        "rsi": 45.2 + random.random() * 10 - 5,  # Neutral RSI with some randomness
        "macd": {
            "macd_line": 0.2 + random.random() * 0.2 - 0.1,
            "signal_line": 0.1 + random.random() * 0.2 - 0.1,
            "histogram": 0.1 + random.random() * 0.2 - 0.1,
            "trending_up": random.choice([True, False])
        },
        "sma": {
            "sma_20": 150.50 + random.random() * 2 - 1,
            "sma_50": 145.30 + random.random() * 2 - 1,
            "sma_200": 140.10 + random.random() * 2 - 1,
            "price_above_sma_20": random.choice([True, False]),
            "price_above_sma_50": random.choice([True, False]),
            "price_above_sma_200": random.choice([True, True, False])  # Biased toward being above SMA200
        },
        "bollinger": {
            "upper": 155.20 + random.random() * 2 - 1,
            "middle": 150.50 + random.random() * 2 - 1,
            "lower": 145.80 + random.random() * 2 - 1,
            "width": 9.40 + random.random() * 1 - 0.5,
            "percent_b": 0.55 + random.random() * 0.2 - 0.1
        }
    }

def _score_to_sentiment(score: float) -> str:
    """Convert a sentiment score to a sentiment label."""
    if score > 0.7:
        return "Very Positive"
    elif score > 0.3:
        return "Positive"
    elif score > -0.3:
        return "Neutral"
    elif score > -0.7:
        return "Negative"
    else:
        return "Very Negative" 