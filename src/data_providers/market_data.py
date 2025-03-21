"""
Market data provider for retrieving real-time and historical market data.
"""
import logging
import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MarketDataProvider:
    """
    Provides market data for trading agents including prices, fundamentals, news, etc.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the market data provider.
        
        Args:
            api_key: API key for external data services
        """
        self.api_key = api_key
        logger.info("Initializing Market Data Provider")
    
    def get_current_price(self, ticker: str) -> float:
        """
        Get the current price for a given ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Current price
        """
        # Mock implementation - in a real system, this would call an external API
        logger.info(f"Fetching current price for {ticker}")
        
        # Simulate a price between $10 and $500
        base_price = hash(ticker) % 490 + 10
        jitter = random.uniform(-0.05, 0.05)  # Add some randomness
        
        return round(base_price * (1 + jitter), 2)
    
    def get_historical_prices(self, 
                             ticker: str, 
                             start_date: datetime, 
                             end_date: datetime) -> List[Dict[str, Any]]:
        """
        Get historical price data for a given ticker.
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date for historical data
            end_date: End date for historical data
            
        Returns:
            List of historical price data points
        """
        logger.info(f"Fetching historical prices for {ticker} from {start_date} to {end_date}")
        
        # Mock implementation - in a real system, this would call an external API
        result = []
        current_date = start_date
        
        # Base price (deterministic based on ticker for consistency)
        base_price = hash(ticker) % 490 + 10
        current_price = base_price
        
        # Generate daily prices
        while current_date <= end_date:
            # Create some random walk price movement
            daily_change = random.normalvariate(0, 0.01)  # Mean 0, std dev 1%
            current_price *= (1 + daily_change)
            
            # Add some volatility based on day of week (higher on Mon/Fri)
            weekday = current_date.weekday()
            if weekday == 0 or weekday == 4:  # Monday or Friday
                volatility = random.uniform(-0.02, 0.02)
                current_price *= (1 + volatility)
            
            # Ensure price doesn't go too low
            current_price = max(current_price, 1.0)
            
            # Create price data point
            price_data = {
                "date": current_date.strftime("%Y-%m-%d"),
                "open": round(current_price * (1 + random.uniform(-0.005, 0.005)), 2),
                "high": round(current_price * (1 + random.uniform(0, 0.02)), 2),
                "low": round(current_price * (1 - random.uniform(0, 0.02)), 2),
                "close": round(current_price, 2),
                "volume": int(random.uniform(100000, 10000000))
            }
            
            result.append(price_data)
            current_date += timedelta(days=1)
            
            # Skip weekends
            while current_date.weekday() > 4:  # 5=Saturday, 6=Sunday
                current_date += timedelta(days=1)
        
        return result
    
    def get_fundamental_data(self, ticker: str) -> Dict[str, Any]:
        """
        Get fundamental data for a given ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Fundamental data including financials, ratios, etc.
        """
        logger.info(f"Fetching fundamental data for {ticker}")
        
        # Mock implementation - in a real system, this would call an external API
        # Seed the random generator with ticker for consistent results
        random.seed(hash(ticker))
        
        # Calculate mock financial metrics with some internal consistency
        revenue = random.uniform(1e6, 1e10)  # $1M to $10B
        profit_margin = random.uniform(0.05, 0.4)  # 5% to 40%
        earnings = revenue * profit_margin
        shares_outstanding = random.uniform(1e6, 5e9)  # 1M to 5B shares
        
        # Current price for market cap calculation
        price = self.get_current_price(ticker)
        market_cap = price * shares_outstanding
        
        # P/E ratio with some reasonable bounds
        pe_ratio = market_cap / (earnings if earnings > 0 else 1e6)
        pe_ratio = min(100, max(5, pe_ratio))  # Keep between 5 and 100
        
        # Book value with reasonable P/B
        pb_ratio = random.uniform(1, 10)
        book_value = market_cap / pb_ratio
        
        # Debt metrics
        debt_to_equity = random.uniform(0, 2.5)
        total_debt = book_value * debt_to_equity
        
        # Dividend data
        pays_dividend = random.random() > 0.5
        dividend_yield = random.uniform(0.01, 0.06) if pays_dividend else 0
        
        # Reset random seed
        random.seed()
        
        return {
            "ticker": ticker,
            "name": f"{ticker} Corporation",
            "sector": random.choice(["Technology", "Healthcare", "Finance", "Consumer", "Energy", "Utilities", "Manufacturing"]),
            "industry": random.choice(["Software", "Hardware", "Banking", "Insurance", "Pharmaceuticals", "Retail", "Oil & Gas"]),
            "financials": {
                "revenue": round(revenue, 2),
                "earnings": round(earnings, 2),
                "profit_margin": round(profit_margin, 4),
                "revenue_growth": round(random.uniform(-0.1, 0.4), 4),
                "free_cash_flow": round(earnings * random.uniform(0.7, 1.3), 2)
            },
            "metrics": {
                "pe_ratio": round(pe_ratio, 2),
                "pb_ratio": round(pb_ratio, 2),
                "price_to_sales": round(market_cap / revenue, 2),
                "debt_to_equity": round(debt_to_equity, 2),
                "total_debt": round(total_debt, 2),
                "shares_outstanding": int(shares_outstanding),
                "market_cap": round(market_cap, 2)
            },
            "dividends": {
                "pays_dividend": pays_dividend,
                "dividend_yield": round(dividend_yield, 4),
                "dividend_amount": round(price * dividend_yield, 2) if pays_dividend else 0
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def get_news_sentiment(self, ticker: str, days: int = 7) -> Dict[str, Any]:
        """
        Get news sentiment data for a given ticker.
        
        Args:
            ticker: Stock ticker symbol
            days: Number of days to look back
            
        Returns:
            News sentiment data including sentiment scores and major headlines
        """
        logger.info(f"Fetching news sentiment for {ticker} over last {days} days")
        
        # Mock implementation - in a real system, this would call an external API
        # Seed the random generator with ticker and date for somewhat consistent results
        random.seed(hash(ticker) + hash(datetime.now().strftime("%Y-%m-%d")))
        
        # Generate mock sentiment data
        sentiment_score = random.uniform(-1, 1)  # -1 very negative, 1 very positive
        
        # Generate mock news headlines based on sentiment
        headlines = []
        sentiment_words = {
            "positive": ["Surges", "Beats Expectations", "Announces Expansion", "Innovative", "Growth", "Partnership", "Dividend Increase"],
            "neutral": ["Announces", "Releases", "Schedules", "Plans", "Appoints", "Updates", "Maintains"],
            "negative": ["Drops", "Misses Expectations", "Cuts Forecast", "Layoffs", "Debt Concerns", "Delays", "Regulatory Issues"]
        }
        
        num_headlines = random.randint(3, 8)
        
        for _ in range(num_headlines):
            # Determine headline sentiment (biased toward overall sentiment)
            headline_bias = random.uniform(-1, 1) + sentiment_score  # Add bias toward overall sentiment
            
            if headline_bias > 0.3:
                word_list = sentiment_words["positive"]
                headline_sentiment = "positive"
            elif headline_bias < -0.3:
                word_list = sentiment_words["negative"]
                headline_sentiment = "negative"
            else:
                word_list = sentiment_words["neutral"]
                headline_sentiment = "neutral"
            
            # Generate headline
            keyword = random.choice(word_list)
            days_ago = random.randint(0, days)
            date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            
            headline = {
                "title": f"{ticker} {keyword} {random.choice(['on Q' + str(random.randint(1, 4)) + ' Results', 'in Market Update', 'amid Industry Changes', 'following Analyst Report'])}",
                "date": date,
                "source": random.choice(["MarketWatch", "Bloomberg", "Reuters", "CNBC", "WSJ", "Financial Times"]),
                "sentiment": headline_sentiment,
                "sentiment_score": round(random.uniform(-1, 1) * (0.7 if headline_sentiment == "neutral" else 1), 2)
            }
            
            headlines.append(headline)
        
        # Sort headlines by date
        headlines.sort(key=lambda x: x["date"], reverse=True)
        
        # Reset random seed
        random.seed()
        
        return {
            "ticker": ticker,
            "overall_sentiment": round(sentiment_score, 2),
            "sentiment_label": "positive" if sentiment_score > 0.2 else "negative" if sentiment_score < -0.2 else "neutral",
            "headlines": headlines,
            "article_count": len(headlines),
            "social_media_mentions": random.randint(100, 10000),
            "period": f"Last {days} days"
        }
    
    def get_market_data_snapshot(self, ticker: str) -> Dict[str, Any]:
        """
        Get a comprehensive market data snapshot for a given ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Comprehensive market data including price, fundamentals, and sentiment
        """
        logger.info(f"Generating market data snapshot for {ticker}")
        
        # Get data from various sources
        current_price = self.get_current_price(ticker)
        
        # Get 1 year of historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        historical_data = self.get_historical_prices(ticker, start_date, end_date)
        
        # Calculate simple technical indicators
        if len(historical_data) > 0:
            latest_price = historical_data[-1]["close"]
            
            # 50-day moving average
            ma_50 = sum(data["close"] for data in historical_data[-50:]) / min(50, len(historical_data))
            
            # 200-day moving average
            ma_200 = sum(data["close"] for data in historical_data[-200:]) / min(200, len(historical_data))
            
            # Relative Strength Index (simplified)
            gains = 0
            losses = 0
            count = min(14, len(historical_data) - 1)
            
            for i in range(len(historical_data) - count, len(historical_data)):
                change = historical_data[i]["close"] - historical_data[i-1]["close"]
                if change > 0:
                    gains += change
                else:
                    losses -= change
            
            if count > 0:
                avg_gain = gains / count
                avg_loss = losses / count
                
                if avg_loss > 0:
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))
                else:
                    rsi = 100
            else:
                rsi = 50
        else:
            latest_price = current_price
            ma_50 = current_price
            ma_200 = current_price
            rsi = 50
        
        # Get other data
        fundamental_data = self.get_fundamental_data(ticker)
        news_sentiment = self.get_news_sentiment(ticker)
        
        # Create technical indicators
        technical_indicators = {
            "price": round(latest_price, 2),
            "ma_50": round(ma_50, 2),
            "ma_200": round(ma_200, 2),
            "rsi": round(rsi, 2),
            "above_ma_50": latest_price > ma_50,
            "above_ma_200": latest_price > ma_200,
            "ma_50_trend": "up" if ma_50 > ma_200 else "down",
            "volume": historical_data[-1]["volume"] if historical_data else 0,
            "price_change_1d": round((latest_price / historical_data[-2]["close"] - 1) * 100, 2) if len(historical_data) > 1 else 0,
            "price_change_1m": round((latest_price / historical_data[-min(22, len(historical_data))]["close"] - 1) * 100, 2) if len(historical_data) >= 22 else 0,
            "price_change_1y": round((latest_price / historical_data[0]["close"] - 1) * 100, 2) if len(historical_data) > 0 else 0
        }
        
        return {
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "current_price": current_price,
            "technical_indicators": technical_indicators,
            "fundamentals": fundamental_data,
            "news_sentiment": news_sentiment
        } 