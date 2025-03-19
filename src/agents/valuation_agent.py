import logging
import random
from typing import Dict, List, Any, Optional
import datetime
import numpy as np

logger = logging.getLogger(__name__)

class ValuationAgent:
    """
    Valuation analysis trading agent.
    
    This agent focuses on:
    - Discounted Cash Flow (DCF) analysis
    - Comparable company analysis
    - Precedent transactions analysis
    - Sum-of-parts valuation
    - Scenario analysis
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Valuation Agent with configuration settings.
        
        Args:
            config: Dictionary containing configuration settings
        """
        self.config = config
        self.name = "Valuation Analysis Agent"
        self.weight = config['agents']['valuation']['weight']
        
        # Cache for valuation data
        self.valuation_data = {}
        self.last_update = {}
        
        # Update frequency (6 hours for valuation data)
        self.update_frequency = datetime.timedelta(hours=6)
        
        # Industry comparables
        self.industry_comps = self._initialize_industry_comps()
        
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
            # Get valuation data
            valuation = self._get_valuation_data(symbol)
            
            if valuation:
                # Generate signal based on valuation analysis
                signal = self._analyze_valuation(symbol, valuation)
                signals[symbol] = signal
            else:
                # Fallback signal if data unavailable
                signals[symbol] = {
                    'action': 'HOLD',
                    'confidence': 0.5,
                    'reasoning': f"Insufficient valuation data for {symbol}",
                    'time_horizon': 180  # 6 months default horizon
                }
        
        return signals
    
    def _get_valuation_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get valuation data for a company.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with valuation data or None if unavailable
        """
        now = datetime.datetime.now()
        
        # Check if we have recent data
        if (symbol in self.valuation_data and 
            symbol in self.last_update and
            now - self.last_update[symbol] < self.update_frequency):
            return self.valuation_data[symbol]
        
        # Get new valuation data
        data = self._calculate_valuation(symbol)
        
        if data:
            # Cache the data
            self.valuation_data[symbol] = data
            self.last_update[symbol] = now
        
        return data
    
    def _initialize_industry_comps(self) -> Dict[str, Dict[str, List[Dict[str, float]]]]:
        """Initialize industry comparable companies data."""
        industries = ['Technology', 'Healthcare', 'Finance', 'Consumer', 'Energy']
        comps = {}
        
        for industry in industries:
            # Generate 10 comparable companies per industry
            companies = []
            for _ in range(10):
                companies.append({
                    'ev_ebitda': random.uniform(8, 20),
                    'pe_ratio': random.uniform(12, 30),
                    'pb_ratio': random.uniform(1, 8),
                    'ps_ratio': random.uniform(1, 10),
                    'ev_revenue': random.uniform(2, 8)
                })
            
            # Calculate median multiples
            medians = {
                'ev_ebitda': np.median([c['ev_ebitda'] for c in companies]),
                'pe_ratio': np.median([c['pe_ratio'] for c in companies]),
                'pb_ratio': np.median([c['pb_ratio'] for c in companies]),
                'ps_ratio': np.median([c['ps_ratio'] for c in companies]),
                'ev_revenue': np.median([c['ev_revenue'] for c in companies])
            }
            
            comps[industry] = {
                'companies': companies,
                'medians': medians
            }
        
        return comps
    
    def _calculate_valuation(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Calculate company valuation using multiple methods.
        
        In a real implementation, this would:
        1. Perform DCF analysis
        2. Calculate comparable company multiples
        3. Analyze precedent transactions
        4. Perform sum-of-parts analysis
        5. Run scenario analysis
        
        For the prototype, we generate simulated data.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with valuation data or None if calculation fails
        """
        try:
            now = datetime.datetime.now()
            
            # Select random industry
            industry = random.choice(['Technology', 'Healthcare', 'Finance', 'Consumer', 'Energy'])
            industry_data = self.industry_comps[industry]
            
            # Current market data
            current_price = random.uniform(10, 1000)
            shares_outstanding = random.uniform(1e8, 1e10)
            market_cap = current_price * shares_outstanding
            net_debt = random.uniform(-market_cap * 0.2, market_cap * 0.4)
            enterprise_value = market_cap + net_debt
            
            # Financial metrics
            revenue = random.uniform(market_cap * 0.1, market_cap * 0.5)
            ebitda = revenue * random.uniform(0.1, 0.3)
            net_income = ebitda * random.uniform(0.4, 0.7)
            book_value = market_cap * random.uniform(0.3, 0.8)
            
            # Calculate current multiples
            current_multiples = {
                'ev_ebitda': enterprise_value / ebitda if ebitda > 0 else None,
                'pe_ratio': current_price / (net_income / shares_outstanding) if net_income > 0 else None,
                'pb_ratio': current_price / (book_value / shares_outstanding) if book_value > 0 else None,
                'ps_ratio': current_price / (revenue / shares_outstanding) if revenue > 0 else None,
                'ev_revenue': enterprise_value / revenue if revenue > 0 else None
            }
            
            # DCF Valuation
            dcf_scenarios = {
                'bear': {
                    'value': current_price * random.uniform(0.6, 0.9),
                    'probability': random.uniform(0.2, 0.4)
                },
                'base': {
                    'value': current_price * random.uniform(0.9, 1.1),
                    'probability': random.uniform(0.4, 0.6)
                },
                'bull': {
                    'value': current_price * random.uniform(1.1, 1.4),
                    'probability': random.uniform(0.2, 0.4)
                }
            }
            
            # Calculate expected DCF value
            dcf_value = sum(
                scenario['value'] * scenario['probability']
                for scenario in dcf_scenarios.values()
            )
            
            # Comparable company valuation
            comp_values = {}
            for multiple, current in current_multiples.items():
                if current is not None:
                    median = industry_data['medians'][multiple]
                    comp_values[multiple] = current / median
            
            # Precedent transactions (simulated)
            transaction_premium = random.uniform(-0.1, 0.3)  # -10% to +30% premium
            
            return {
                'symbol': symbol,
                'timestamp': now.isoformat(),
                'industry': industry,
                'current_price': current_price,
                'market_data': {
                    'shares_outstanding': shares_outstanding,
                    'market_cap': market_cap,
                    'enterprise_value': enterprise_value,
                    'net_debt': net_debt
                },
                'financials': {
                    'revenue': revenue,
                    'ebitda': ebitda,
                    'net_income': net_income,
                    'book_value': book_value
                },
                'current_multiples': current_multiples,
                'industry_medians': industry_data['medians'],
                'dcf_analysis': {
                    'scenarios': dcf_scenarios,
                    'expected_value': dcf_value
                },
                'comp_analysis': comp_values,
                'transaction_premium': transaction_premium
            }
        except Exception as e:
            logger.error(f"Error calculating valuation for {symbol}: {e}")
            return None
    
    def _analyze_valuation(self, symbol: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze valuation data and generate a trading signal.
        
        Args:
            symbol: Stock symbol
            data: Valuation data dictionary
            
        Returns:
            Signal dictionary
        """
        # Calculate component scores
        dcf_score = self._calculate_dcf_score(data)
        multiple_score = self._calculate_multiple_score(data)
        premium_score = self._calculate_premium_score(data)
        
        # Calculate weighted valuation score
        valuation_score = (
            dcf_score * 0.5 +
            multiple_score * 0.4 +
            premium_score * 0.1
        )
        
        # Generate signal based on valuation score
        if valuation_score > 0.7:  # Significantly undervalued
            action = 'BUY'
            confidence = valuation_score
            time_horizon = 365  # 1 year
            reasoning = [
                f"DCF analysis indicates undervaluation (score: {dcf_score:.2f})",
                f"Trading at discount to peers (score: {multiple_score:.2f})",
                f"Attractive vs recent transactions (score: {premium_score:.2f})",
                f"Expected upside: {((1/valuation_score - 1) * 100):.1f}%"
            ]
        
        elif valuation_score < 0.3:  # Significantly overvalued
            action = 'SELL'
            confidence = 0.6 + (0.3 - valuation_score)
            time_horizon = 180  # 6 months
            reasoning = [
                f"DCF analysis indicates overvaluation (score: {dcf_score:.2f})",
                f"Trading at premium to peers (score: {multiple_score:.2f})",
                f"Rich vs recent transactions (score: {premium_score:.2f})",
                f"Expected downside: {((valuation_score/0.3 - 1) * -100):.1f}%"
            ]
        
        else:  # Fairly valued
            action = 'HOLD'
            confidence = 0.5
            time_horizon = 90  # 3 months
            reasoning = [
                f"DCF value near current price (score: {dcf_score:.2f})",
                f"In-line with peer multiples (score: {multiple_score:.2f})",
                f"Fair value range: ±10%"
            ]
        
        return {
            'action': action,
            'confidence': min(confidence, 0.95),
            'reasoning': reasoning,
            'time_horizon': time_horizon,
            'analysis': {
                'valuation_score': valuation_score,
                'dcf_score': dcf_score,
                'multiple_score': multiple_score,
                'premium_score': premium_score,
                'current_price': data['current_price'],
                'dcf_value': data['dcf_analysis']['expected_value']
            }
        }
    
    def _calculate_dcf_score(self, data: Dict[str, Any]) -> float:
        """Calculate score based on DCF analysis."""
        current_price = data['current_price']
        dcf_value = data['dcf_analysis']['expected_value']
        
        # Calculate upside/downside
        if dcf_value > current_price:
            # Undervalued
            upside = (dcf_value / current_price) - 1
            score = min(0.5 + (upside * 2), 1.0)  # 25% upside -> score of 1.0
        else:
            # Overvalued
            downside = 1 - (dcf_value / current_price)
            score = max(0.5 - (downside * 2), 0.0)  # 25% downside -> score of 0.0
        
        return score
    
    def _calculate_multiple_score(self, data: Dict[str, Any]) -> float:
        """Calculate score based on comparable company analysis."""
        comp_values = data['comp_analysis']
        if not comp_values:
            return 0.5  # Neutral if no comparable data
        
        # Calculate average relative multiple
        relative_multiples = list(comp_values.values())
        avg_relative = np.mean(relative_multiples)
        
        # Score based on relative valuation
        # avg_relative < 1 means trading at discount to peers
        if avg_relative < 1:
            score = 0.5 + min((1 - avg_relative) * 2, 0.5)  # 25% discount -> score of 1.0
        else:
            score = 0.5 - min((avg_relative - 1) * 2, 0.5)  # 25% premium -> score of 0.0
        
        return score
    
    def _calculate_premium_score(self, data: Dict[str, Any]) -> float:
        """Calculate score based on transaction premium analysis."""
        premium = data['transaction_premium']
        
        # Score based on premium to recent transactions
        # Negative premium means trading below transaction values
        if premium < 0:
            score = 0.5 + min(abs(premium) * 2, 0.5)  # 25% discount -> score of 1.0
        else:
            score = 0.5 - min(premium * 2, 0.5)  # 25% premium -> score of 0.0
        
        return score
