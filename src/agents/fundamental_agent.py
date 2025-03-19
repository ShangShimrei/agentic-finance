import logging
import random
from typing import Dict, List, Any, Optional
import datetime
import numpy as np

logger = logging.getLogger(__name__)

class FundamentalAgent:
    """
    Fundamental analysis trading agent.
    
    This agent focuses on:
    - Financial statement analysis
    - Key financial ratios and metrics
    - Industry comparison
    - Growth trends and projections
    - Quality of earnings
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Fundamental Agent with configuration settings.
        
        Args:
            config: Dictionary containing configuration settings
        """
        self.config = config
        self.name = "Fundamental Analysis Agent"
        self.weight = config['agents']['fundamental']['weight']
        
        # Cache for fundamental data
        self.fundamental_data = {}
        self.last_update = {}
        
        # Update frequency (4 hours for fundamental data)
        self.update_frequency = datetime.timedelta(hours=4)
        
        # Industry averages (simulated)
        self.industry_averages = self._initialize_industry_averages()
        
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
            # Get fundamental data
            fundamentals = self._get_fundamental_data(symbol)
            
            if fundamentals:
                # Analyze fundamentals and generate signal
                signal = self._analyze_fundamentals(symbol, fundamentals)
                signals[symbol] = signal
            else:
                # Fallback signal if data unavailable
                signals[symbol] = {
                    'action': 'HOLD',
                    'confidence': 0.5,
                    'reasoning': f"Insufficient fundamental data for {symbol}",
                    'time_horizon': 180  # 6 months default horizon
                }
        
        return signals
    
    def _get_fundamental_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get fundamental data for a company.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with fundamental data or None if unavailable
        """
        now = datetime.datetime.now()
        
        # Check if we have recent data
        if (symbol in self.fundamental_data and 
            symbol in self.last_update and
            now - self.last_update[symbol] < self.update_frequency):
            return self.fundamental_data[symbol]
        
        # Get new fundamental data
        data = self._fetch_fundamental_data(symbol)
        
        if data:
            # Cache the data
            self.fundamental_data[symbol] = data
            self.last_update[symbol] = now
        
        return data
    
    def _fetch_fundamental_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetch fundamental data for a company.
        
        In a real implementation, this would call a financial data API.
        For the prototype, we generate simulated data.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with fundamental data or None if unavailable
        """
        try:
            # Generate simulated fundamental data
            industry = random.choice(['Technology', 'Healthcare', 'Finance', 'Consumer', 'Energy'])
            industry_avg = self.industry_averages[industry]
            now = datetime.datetime.now()
            
            return {
                'symbol': symbol,
                'industry': industry,
                'market_cap': random.uniform(1e9, 1e12),  # $1B to $1T
                'revenue': random.uniform(1e8, 1e11),
                'revenue_growth': random.uniform(-0.1, 0.4),
                'gross_margin': random.uniform(0.2, 0.8),
                'operating_margin': random.uniform(0.05, 0.3),
                'net_margin': random.uniform(0.02, 0.25),
                'pe_ratio': random.uniform(8, 40),
                'pb_ratio': random.uniform(1, 10),
                'debt_to_equity': random.uniform(0, 2),
                'current_ratio': random.uniform(1, 3),
                'quick_ratio': random.uniform(0.5, 2),
                'roe': random.uniform(0.05, 0.3),
                'roa': random.uniform(0.02, 0.15),
                'fcf_growth': random.uniform(-0.2, 0.5),
                'earnings_quality': random.uniform(0.5, 1.0),
                'dividend_yield': random.uniform(0, 0.05),
                'payout_ratio': random.uniform(0, 0.8),
                'industry_averages': industry_avg,
                'timestamp': now.isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching fundamental data for {symbol}: {e}")
            return None
    
    def _initialize_industry_averages(self) -> Dict[str, Dict[str, float]]:
        """Initialize simulated industry average metrics."""
        industries = ['Technology', 'Healthcare', 'Finance', 'Consumer', 'Energy']
        averages = {}
        
        for industry in industries:
            averages[industry] = {
                'pe_ratio': random.uniform(15, 30),
                'pb_ratio': random.uniform(2, 6),
                'operating_margin': random.uniform(0.1, 0.25),
                'revenue_growth': random.uniform(0.05, 0.2),
                'roe': random.uniform(0.08, 0.2),
                'debt_to_equity': random.uniform(0.5, 1.5)
            }
        
        return averages
    
    def _analyze_fundamentals(self, symbol: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze fundamental data and generate a trading signal.
        
        Args:
            symbol: Stock symbol
            data: Fundamental data dictionary
            
        Returns:
            Signal dictionary
        """
        # Get industry averages
        industry_avg = data['industry_averages']
        
        # Calculate component scores
        profitability_score = self._calculate_profitability_score(data, industry_avg)
        growth_score = self._calculate_growth_score(data, industry_avg)
        valuation_score = self._calculate_valuation_score(data, industry_avg)
        financial_health_score = self._calculate_financial_health_score(data)
        quality_score = self._calculate_quality_score(data)
        
        # Calculate weighted overall score
        overall_score = (
            profitability_score * 0.25 +
            growth_score * 0.25 +
            valuation_score * 0.20 +
            financial_health_score * 0.15 +
            quality_score * 0.15
        )
        
        # Generate signal based on overall score
        if overall_score > 0.7:  # Strong fundamentals
            action = 'BUY'
            confidence = overall_score
            time_horizon = 365  # 1 year
            reasoning = [
                f"Strong profitability metrics (score: {profitability_score:.2f})",
                f"Robust growth profile (score: {growth_score:.2f})",
                f"Attractive valuation (score: {valuation_score:.2f})",
                f"Solid financial health (score: {financial_health_score:.2f})"
            ]
        elif overall_score < 0.4:  # Weak fundamentals
            action = 'SELL'
            confidence = 0.6 + (0.4 - overall_score)
            time_horizon = 90  # 3 months
            reasoning = [
                f"Poor profitability metrics (score: {profitability_score:.2f})",
                f"Weak growth profile (score: {growth_score:.2f})",
                f"Concerning valuation (score: {valuation_score:.2f})",
                f"Financial health issues (score: {financial_health_score:.2f})"
            ]
        else:  # Average fundamentals
            action = 'HOLD'
            confidence = 0.5
            time_horizon = 180  # 6 months
            reasoning = [
                f"Average fundamental metrics",
                f"Moderate growth prospects (score: {growth_score:.2f})",
                f"Fair valuation (score: {valuation_score:.2f})"
            ]
        
        return {
            'action': action,
            'confidence': min(confidence, 0.95),
            'reasoning': reasoning,
            'time_horizon': time_horizon,
            'analysis': {
                'overall_score': overall_score,
                'profitability_score': profitability_score,
                'growth_score': growth_score,
                'valuation_score': valuation_score,
                'financial_health_score': financial_health_score,
                'quality_score': quality_score
            }
        }
    
    def _calculate_profitability_score(self, data: Dict[str, Any], industry_avg: Dict[str, float]) -> float:
        """Calculate profitability score based on margins and returns."""
        operating_margin_vs_industry = data['operating_margin'] / industry_avg['operating_margin']
        
        scores = [
            data['operating_margin'] / 0.3,  # Normalize to 30% margin
            data['net_margin'] / 0.2,        # Normalize to 20% margin
            data['roe'] / industry_avg['roe'],
            data['roa'] / 0.1,               # Normalize to 10% ROA
            operating_margin_vs_industry
        ]
        
        return np.clip(np.mean(scores), 0, 1)
    
    def _calculate_growth_score(self, data: Dict[str, Any], industry_avg: Dict[str, float]) -> float:
        """Calculate growth score based on revenue and cash flow growth."""
        revenue_growth_vs_industry = data['revenue_growth'] / industry_avg['revenue_growth']
        
        scores = [
            (data['revenue_growth'] + 0.1) / 0.5,  # Normalize to 50% growth
            (data['fcf_growth'] + 0.2) / 0.7,      # Normalize to 70% growth
            revenue_growth_vs_industry
        ]
        
        return np.clip(np.mean(scores), 0, 1)
    
    def _calculate_valuation_score(self, data: Dict[str, Any], industry_avg: Dict[str, float]) -> float:
        """Calculate valuation score based on price multiples."""
        pe_vs_industry = industry_avg['pe_ratio'] / data['pe_ratio']  # Inverted for lower is better
        pb_vs_industry = industry_avg['pb_ratio'] / data['pb_ratio']  # Inverted for lower is better
        
        scores = [
            pe_vs_industry,
            pb_vs_industry,
            data['dividend_yield'] / 0.05  # Normalize to 5% yield
        ]
        
        return np.clip(np.mean(scores), 0, 1)
    
    def _calculate_financial_health_score(self, data: Dict[str, Any]) -> float:
        """Calculate financial health score based on liquidity and leverage."""
        scores = [
            1 - (data['debt_to_equity'] / 2),  # Lower is better, normalized to 200% D/E
            data['current_ratio'] / 2,         # Normalize to 2.0 ratio
            data['quick_ratio'] / 1.5,         # Normalize to 1.5 ratio
            1 - data['payout_ratio']           # Lower is better for sustainability
        ]
        
        return np.clip(np.mean(scores), 0, 1)
    
    def _calculate_quality_score(self, data: Dict[str, Any]) -> float:
        """Calculate quality score based on earnings quality and stability."""
        return data['earnings_quality']  # Already normalized 0-1
