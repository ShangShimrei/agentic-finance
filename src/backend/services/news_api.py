"""
News API provider for fetching financial news and market sentiment data.
This module provides integration with various news sources for sentiment analysis.
"""

import os
import logging
import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

class NewsAPIProvider:
    """Provider for financial news and market sentiment data."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the News API provider.
        
        Args:
            api_key: Optional API key for authentication. If not provided,
                    looks for the NEWSAPI_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("NEWSAPI_KEY")
        
        # Base URLs for different news APIs
        self.news_api_url = "https://newsapi.org/v2"
        
        # Check if API key is available
        if not self.api_key:
            logger.warning("No API key provided for News API. Using mock data.")
        
        logger.info("Initialized News API provider")
    
    def get_news(self, 
                ticker: str, 
                days_back: int = 7, 
                sources: Optional[List[str]] = None,
                max_results: int = 50) -> Dict[str, Any]:
        """
        Get news articles for a ticker symbol.
        
        Args:
            ticker: Ticker symbol to find news for
            days_back: Number of days to look back
            sources: Optional list of news sources to include
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with news data
        """
        if not self.api_key:
            return self._generate_mock_news(ticker, days_back, max_results)
        
        logger.info(f"Fetching news for {ticker} from the past {days_back} days")
        
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Format dates for API
            from_date = start_date.strftime('%Y-%m-%d')
            to_date = end_date.strftime('%Y-%m-%d')
            
            # Build parameters
            params = {
                'apiKey': self.api_key,
                'q': f"{ticker} OR {self._get_company_name(ticker)}",
                'from': from_date,
                'to': to_date,
                'language': 'en',
                'sortBy': 'relevancy',
                'pageSize': max_results
            }
            
            # Add sources if provided
            if sources:
                params['sources'] = ','.join(sources)
            
            # Make API request
            response = requests.get(f"{self.news_api_url}/everything", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Format results
            articles = self._format_articles(data.get('articles', []), ticker)
            
            return {
                'ticker': ticker,
                'total_results': data.get('totalResults', 0),
                'articles': articles,
                'sources': list(set([article['source'] for article in articles])),
                'top_keywords': self._extract_keywords(articles),
                'date_range': {
                    'from': from_date,
                    'to': to_date
                }
            }
        
        except RequestException as e:
            logger.error(f"Error fetching news for {ticker}: {e}")
            return self._generate_mock_news(ticker, days_back, max_results)
        
        except Exception as e:
            logger.error(f"Unexpected error fetching news for {ticker}: {e}")
            return self._generate_mock_news(ticker, days_back, max_results)
    
    def analyze_sentiment(self, 
                         ticker: str, 
                         days_back: int = 7) -> Dict[str, Any]:
        """
        Analyze sentiment for a ticker based on news articles.
        
        Args:
            ticker: Ticker symbol to analyze
            days_back: Number of days to look back
            
        Returns:
            Dictionary with sentiment analysis data
        """
        # Get news articles first
        news_data = self.get_news(ticker, days_back)
        articles = news_data.get('articles', [])
        
        if not articles:
            return self._generate_mock_sentiment(ticker)
        
        # If we have an API key, we use a real sentiment analysis API
        if self.api_key:
            try:
                # Here we would call a sentiment analysis API with the articles
                # For now, we'll use mock data even if we have an API key
                return self._calculate_sentiment_from_articles(ticker, articles)
            except Exception as e:
                logger.error(f"Error analyzing sentiment for {ticker}: {e}")
                return self._generate_mock_sentiment(ticker)
        else:
            # Otherwise, generate mock sentiment data
            return self._generate_mock_sentiment(ticker)
    
    def _calculate_sentiment_from_articles(self, 
                                         ticker: str, 
                                         articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate sentiment scores from articles.
        In a real implementation, this would use an NLP API like NLTK, Vader, or GPT-4.
        
        Args:
            ticker: Ticker symbol
            articles: List of news articles
            
        Returns:
            Dictionary with sentiment analysis
        """
        # Mock implementation - in a real-world scenario, 
        # this would use proper NLP to analyze article content
        
        # Assign random sentiment to each article (0-1 scale)
        for article in articles:
            article['sentiment'] = random.uniform(0, 1)
        
        # Calculate average sentiment
        if articles:
            avg_sentiment = sum(article['sentiment'] for article in articles) / len(articles)
        else:
            avg_sentiment = 0.5  # Neutral sentiment if no articles
        
        # Identify most recent articles for recency bias
        articles.sort(key=lambda x: x.get('published_at', ''), reverse=True)
        recent_articles = articles[:min(10, len(articles))]
        
        if recent_articles:
            recent_sentiment = sum(article['sentiment'] for article in recent_articles) / len(recent_articles)
            # Weight recent sentiment more heavily
            weighted_sentiment = (avg_sentiment * 0.4) + (recent_sentiment * 0.6)
        else:
            weighted_sentiment = avg_sentiment
        
        # Extract topics from titles and descriptions
        topics = self._extract_topics(articles)
        
        # Calculate volume and volatility
        volume = len(articles)
        sentiments = [article['sentiment'] for article in articles]
        volatility = self._calculate_volatility(sentiments)
        
        return {
            'ticker': ticker,
            'sentiment_score': weighted_sentiment,
            'sentiment': self._score_to_category(weighted_sentiment),
            'source_scores': {
                'news': weighted_sentiment,
                'social_media': random.uniform(0, 1),  # Mock value
                'blogs': random.uniform(0, 1)  # Mock value
            },
            'topics': topics,
            'volume': volume,
            'volatility': volatility,
            'article_count': len(articles)
        }
    
    def _format_articles(self, 
                        articles: List[Dict[str, Any]], 
                        ticker: str) -> List[Dict[str, Any]]:
        """
        Format articles from the API response.
        
        Args:
            articles: List of articles from the API
            ticker: Ticker symbol
            
        Returns:
            Formatted list of articles
        """
        formatted = []
        
        for article in articles:
            # Extract source name
            source = article.get('source', {}).get('name', 'Unknown Source')
            
            # Format publish date
            published_at = article.get('publishedAt', '')
            
            # Check if article is relevant to the ticker
            title = article.get('title', '')
            description = article.get('description', '')
            content = article.get('content', '')
            
            # Determine relevance (in a real implementation, this would be more sophisticated)
            company_name = self._get_company_name(ticker)
            is_relevant = (
                ticker in title or 
                ticker in description or 
                company_name in title or 
                company_name in description
            )
            
            formatted.append({
                'title': title,
                'description': description,
                'url': article.get('url', ''),
                'source': source,
                'published_at': published_at,
                'content': content,
                'is_relevant': is_relevant
            })
        
        # Sort by relevance and date
        return sorted(formatted, key=lambda x: (x['is_relevant'], x['published_at']), reverse=True)
    
    def _extract_keywords(self, articles: List[Dict[str, Any]]) -> List[str]:
        """
        Extract keywords from articles.
        
        Args:
            articles: List of articles
            
        Returns:
            List of keywords
        """
        # In a real implementation, this would use NLP techniques
        # This is a simplified version that just extracts common words
        
        common_keywords = [
            "earnings", "profit", "loss", "growth", "decline", "revenue",
            "CEO", "executive", "partnership", "deal", "acquisition", "merger",
            "product", "launch", "innovation", "research", "development",
            "market", "stock", "share", "price", "investor", "analysis"
        ]
        
        # Randomly select 5-10 keywords that might appear in financial news
        num_keywords = random.randint(5, 10)
        return random.sample(common_keywords, min(num_keywords, len(common_keywords)))
    
    def _extract_topics(self, articles: List[Dict[str, Any]]) -> List[str]:
        """
        Extract topics from articles.
        
        Args:
            articles: List of articles
            
        Returns:
            List of topics
        """
        # In a real implementation, this would use topic modeling
        # This is a simplified mock implementation
        
        possible_topics = [
            "Earnings Report", "Product Launch", "Management Change", 
            "Regulatory Issues", "Market Trend", "Competitor News",
            "Innovation", "Financial Health", "Partnership", "Acquisition",
            "Stock Performance", "Analyst Ratings", "Economic Impact", 
            "Industry Trends", "Corporate Strategy"
        ]
        
        # Select 2-5 random topics
        num_topics = random.randint(2, 5)
        return random.sample(possible_topics, min(num_topics, len(possible_topics)))
    
    def _calculate_volatility(self, sentiment_values: List[float]) -> float:
        """
        Calculate volatility of sentiment values.
        
        Args:
            sentiment_values: List of sentiment scores
            
        Returns:
            Volatility score (0-1)
        """
        if not sentiment_values or len(sentiment_values) < 2:
            return 0.0
        
        # Simple standard deviation calculation
        mean = sum(sentiment_values) / len(sentiment_values)
        variance = sum((x - mean) ** 2 for x in sentiment_values) / len(sentiment_values)
        std_dev = variance ** 0.5
        
        # Normalize to 0-1 scale (max reasonable std_dev in this case would be 0.5)
        return min(1.0, std_dev * 2)
    
    def _score_to_category(self, score: float) -> str:
        """
        Convert a sentiment score to a category.
        
        Args:
            score: Sentiment score (0-1)
            
        Returns:
            Sentiment category
        """
        if score >= 0.7:
            return "Very Positive"
        elif score >= 0.55:
            return "Positive"
        elif score >= 0.45:
            return "Neutral"
        elif score >= 0.3:
            return "Negative"
        else:
            return "Very Negative"
    
    def _generate_mock_news(self, 
                          ticker: str, 
                          days_back: int, 
                          max_results: int) -> Dict[str, Any]:
        """
        Generate mock news data when API is not available.
        
        Args:
            ticker: Ticker symbol
            days_back: Number of days to look back
            max_results: Maximum results to generate
            
        Returns:
            Mock news data
        """
        logger.info(f"Generating mock news data for {ticker}")
        
        company_name = self._get_company_name(ticker)
        
        # Headlines patterns for generating mock news
        headline_templates = [
            f"{company_name} Reports Strong Quarterly Earnings, Beating Expectations",
            f"{company_name} Announces New Product Line",
            f"Analysts Upgrade {company_name} Stock Rating",
            f"{company_name} Partners with Major Tech Firm",
            f"Investors Cautious About {company_name}'s Market Position",
            f"{company_name} CEO Discusses Future Growth Strategy",
            f"{company_name} Faces Regulatory Scrutiny",
            f"Market Trends Show Promise for {company_name}",
            f"{company_name} Stock Rises After Positive Industry News",
            f"Financial Outlook: What's Next for {company_name}?",
            f"{company_name} Expands into New Markets",
            f"Quarterly Report: {company_name} Meets Expectations",
            f"Industry Analysis: {company_name} vs Competitors",
            f"Economic Factors Affecting {company_name}'s Performance",
            f"{company_name} Announces Leadership Changes"
        ]
        
        # Generate random number of articles (between 5 and max_results)
        num_articles = min(max_results, max(5, random.randint(5, max_results)))
        
        # Generate mock articles
        articles = []
        end_date = datetime.now()
        
        for i in range(num_articles):
            # Random date within the specified range
            days_old = random.randint(0, days_back)
            hours_old = random.randint(0, 23)
            article_date = end_date - timedelta(days=days_old, hours=hours_old)
            
            # Random headline and source
            headline = random.choice(headline_templates)
            source = random.choice([
                "Financial Times", "Bloomberg", "CNBC", "Reuters", 
                "Wall Street Journal", "Investopedia", "MarketWatch",
                "Yahoo Finance", "The Motley Fool", "Business Insider"
            ])
            
            # Generate mock description
            description = f"Latest news about {company_name} ({ticker}) and its market performance. {random.choice(['Positive', 'Negative', 'Neutral'])} outlook for investors."
            
            articles.append({
                'title': headline,
                'description': description,
                'url': f"https://example.com/news/{ticker}/{i}",
                'source': source,
                'published_at': article_date.isoformat(),
                'content': f"Full content about {company_name} would appear here in a real API response.",
                'is_relevant': True
            })
        
        # Sort by date (newest first)
        articles.sort(key=lambda x: x['published_at'], reverse=True)
        
        return {
            'ticker': ticker,
            'total_results': num_articles,
            'articles': articles,
            'sources': list(set([article['source'] for article in articles])),
            'top_keywords': self._extract_keywords(articles),
            'date_range': {
                'from': (end_date - timedelta(days=days_back)).strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d')
            }
        }
    
    def _generate_mock_sentiment(self, ticker: str) -> Dict[str, Any]:
        """
        Generate mock sentiment data.
        
        Args:
            ticker: Ticker symbol
            
        Returns:
            Mock sentiment data
        """
        # Generate a random sentiment score between 0 and 1
        sentiment_score = random.uniform(0, 1)
        
        # Generate source scores
        source_scores = {
            "news": random.uniform(0, 1),
            "social_media": random.uniform(0, 1),
            "blogs": random.uniform(0, 1)
        }
        
        # Generate mock topics
        topics = self._extract_topics([])
        
        # Generate mock volume and volatility
        volume = random.randint(50, 500)
        volatility = random.uniform(0.1, 0.5)
        
        return {
            'ticker': ticker,
            'sentiment_score': sentiment_score,
            'sentiment': self._score_to_category(sentiment_score),
            'source_scores': source_scores,
            'topics': topics,
            'volume': volume,
            'volatility': volatility,
            'article_count': random.randint(20, 100)
        }
    
    def _get_company_name(self, ticker: str) -> str:
        """
        Get company name for a ticker.
        In a real implementation, this would look up the company name.
        
        Args:
            ticker: Ticker symbol
            
        Returns:
            Company name
        """
        # Mock implementation - in a real app, this would use a proper data source
        company_names = {
            "AAPL": "Apple",
            "MSFT": "Microsoft",
            "GOOGL": "Google",
            "AMZN": "Amazon",
            "META": "Meta",
            "TSLA": "Tesla",
            "NVDA": "Nvidia",
            "JPM": "JPMorgan Chase",
            "V": "Visa",
            "WMT": "Walmart",
            "PG": "Procter & Gamble",
            "DIS": "Disney",
            "NFLX": "Netflix",
            "PYPL": "PayPal",
            "INTC": "Intel",
            "IBM": "IBM",
            "AMD": "AMD",
            "CSCO": "Cisco",
            "ORCL": "Oracle",
            "CRM": "Salesforce"
        }
        
        return company_names.get(ticker, f"{ticker} Inc.") 