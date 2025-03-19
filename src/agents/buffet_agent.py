import logging
import random
import requests
from typing import Dict, List, Any, Optional
import os
import json

logger = logging.getLogger(__name__)

class BuffetAgent:
    """
    Buffet-style trading agent that mimics long-term value investing strategies.
    
    This agent focuses on:
    - Companies with strong fundamentals
    - Long-term business prospects
    - Companies trading below their intrinsic value
    - Businesses with economic moats
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Buffet Agent with configuration settings.
        
        Args:
            config: Dictionary containing configuration settings
        """
        self.config = config
        self.name = "Buffet-style Value Agent"
        self.weight = config['agents']['buffet']['weight']
        self.model = config['agents']['buffet']['model']
        self.ollama_url = config['api_keys']['ollama']['base_url']
        
        # For demo purposes, maintain a simple cache of company fundamentals
        self.company_fundamentals = {}
        
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
                - time_horizon: Long-term investment horizon (in days)
        """
        signals = {}
        
        for symbol in symbols:
            # In a real implementation, we would:
            # 1. Get financial data for the company
            # 2. Calculate intrinsic value
            # 3. Compare to current market price
            # 4. Check for economic moat indicators
            # 5. Generate a reasoned decision
            
            # For this prototype, we'll use the Ollama API to generate a simulated analysis
            fundamentals = self._get_company_fundamentals(symbol)
            
            if fundamentals:
                # Use the local LLM to analyze and make a decision
                analysis = self._analyze_with_llm(symbol, fundamentals)
                
                # Parse the LLM output to extract the trading signal
                signal = self._parse_llm_output(analysis)
                signals[symbol] = signal
            else:
                # If we can't get fundamentals, generate a placeholder signal
                signals[symbol] = {
                    'action': 'HOLD',
                    'confidence': 0.5,
                    'reasoning': f"Insufficient fundamental data for {symbol}",
                    'time_horizon': 365  # Buffet is a long-term investor
                }
        
        return signals
    
    def _get_company_fundamentals(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get fundamental data for a company.
        
        In a real implementation, this would call a financial data API.
        For the prototype, we'll use simulated data.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary of fundamental data or None if unavailable
        """
        # Check if we have cached data
        if symbol in self.company_fundamentals:
            return self.company_fundamentals[symbol]
        
        # For the prototype, generate some sample fundamentals
        # In a real implementation, this would call a financial data API
        fundamentals = self._generate_sample_fundamentals(symbol)
        
        # Cache the data
        self.company_fundamentals[symbol] = fundamentals
        return fundamentals
    
    def _generate_sample_fundamentals(self, symbol: str) -> Dict[str, Any]:
        """Generate sample fundamental data for demonstration purposes."""
        # In a real implementation, this would be replaced with actual API calls
        return {
            'symbol': symbol,
            'name': f"{symbol} Inc.",
            'sector': random.choice(['Technology', 'Healthcare', 'Finance', 'Consumer', 'Energy']),
            'market_cap': random.uniform(1e9, 1e12),  # $1B to $1T
            'pe_ratio': random.uniform(8, 30),
            'pb_ratio': random.uniform(1, 10),
            'dividend_yield': random.uniform(0, 0.05),
            'revenue_growth': random.uniform(-0.1, 0.3),
            'profit_margin': random.uniform(0.05, 0.3),
            'debt_to_equity': random.uniform(0, 2),
            'free_cash_flow': random.uniform(-1e9, 5e9),
            'roe': random.uniform(0.05, 0.30),  # Return on Equity
            'current_price': random.uniform(50, 500),
            'intrinsic_value_estimate': random.uniform(40, 600),
        }
    
    def _analyze_with_llm(self, symbol: str, fundamentals: Dict[str, Any]) -> str:
        """
        Use the local LLM to analyze fundamentals and generate a trading decision.
        
        Args:
            symbol: Stock symbol
            fundamentals: Dictionary of fundamental data
            
        Returns:
            LLM response with analysis and decision
        """
        # In a real implementation, this would call the Ollama API
        # For the prototype, we'll simulate the response
        try:
            # Construct a prompt for the LLM
            prompt = self._construct_prompt(symbol, fundamentals)
            
            # Call Ollama API
            # In a real implementation, uncomment this code and use the actual API
            """
            response = requests.post(
                f"{self.ollama_url}/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            )
            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                logger.error(f"Failed to call Ollama API: {response.status_code}")
                return self._generate_fallback_analysis(symbol, fundamentals)
            """
            
            # For now, return a simulated analysis
            return self._generate_fallback_analysis(symbol, fundamentals)
            
        except Exception as e:
            logger.error(f"Error calling Ollama API: {e}")
            return self._generate_fallback_analysis(symbol, fundamentals)
    
    def _construct_prompt(self, symbol: str, fundamentals: Dict[str, Any]) -> str:
        """Construct a prompt for the LLM based on fundamentals."""
        return f"""
        As Warren Buffett, analyze {symbol} ({fundamentals['name']}) for a long-term value investment.
        
        Company Information:
        - Sector: {fundamentals['sector']}
        - Market Cap: ${fundamentals['market_cap'] / 1e9:.2f}B
        - P/E Ratio: {fundamentals['pe_ratio']:.2f}
        - P/B Ratio: {fundamentals['pb_ratio']:.2f}
        - Dividend Yield: {fundamentals['dividend_yield'] * 100:.2f}%
        - Revenue Growth: {fundamentals['revenue_growth'] * 100:.2f}%
        - Profit Margin: {fundamentals['profit_margin'] * 100:.2f}%
        - Debt to Equity: {fundamentals['debt_to_equity']:.2f}
        - Return on Equity: {fundamentals['roe'] * 100:.2f}%
        - Current Price: ${fundamentals['current_price']:.2f}
        - Estimated Intrinsic Value: ${fundamentals['intrinsic_value_estimate']:.2f}
        
        Consider the company's economic moat, management quality, long-term growth prospects, and margin of safety.
        
        Provide a buy, sell, or hold recommendation with:
        1. Action (BUY, SELL, or HOLD)
        2. Confidence level (0.0 to 1.0)
        3. Reasoning (2-3 sentences)
        4. Time horizon (in days)
        """
    
    def _generate_fallback_analysis(self, symbol: str, fundamentals: Dict[str, Any]) -> str:
        """Generate a fallback analysis if the LLM call fails."""
        current_price = fundamentals['current_price']
        intrinsic_value = fundamentals['intrinsic_value_estimate']
        margin_of_safety = (intrinsic_value - current_price) / intrinsic_value
        
        if margin_of_safety > 0.3 and fundamentals['pe_ratio'] < 15:
            action = "BUY"
            confidence = 0.7 + (margin_of_safety * 0.3)
            reasoning = f"{symbol} is trading significantly below its intrinsic value with a strong margin of safety. The company has solid fundamentals with good profit margins and return on equity."
        elif margin_of_safety < -0.2:
            action = "SELL"
            confidence = 0.6 + (abs(margin_of_safety) * 0.2)
            reasoning = f"{symbol} appears overvalued compared to its intrinsic value. The current price does not provide an adequate margin of safety for a value investor."
        else:
            action = "HOLD"
            confidence = 0.5
            reasoning = f"{symbol} is trading close to its intrinsic value. The company has reasonable fundamentals but does not present a compelling buying opportunity at current prices."
        
        return f"""
        Action: {action}
        Confidence: {min(confidence, 0.95):.2f}
        Reasoning: {reasoning}
        Time Horizon: 1825 days
        """
    
    def _parse_llm_output(self, llm_output: str) -> Dict[str, Any]:
        """Parse the LLM output to extract structured signal data."""
        lines = llm_output.strip().split('\n')
        
        signal = {
            'action': 'HOLD',
            'confidence': 0.5,
            'reasoning': '',
            'time_horizon': 365  # Default to 1 year
        }
        
        for line in lines:
            line = line.strip()
            if line.startswith('Action:'):
                action = line.replace('Action:', '').strip().upper()
                if action in ['BUY', 'SELL', 'HOLD']:
                    signal['action'] = action
            
            elif line.startswith('Confidence:'):
                try:
                    confidence = float(line.replace('Confidence:', '').strip())
                    signal['confidence'] = min(max(confidence, 0), 1)  # Ensure it's between 0 and 1
                except ValueError:
                    pass
            
            elif line.startswith('Reasoning:'):
                signal['reasoning'] = line.replace('Reasoning:', '').strip()
            
            elif line.startswith('Time Horizon:'):
                try:
                    time_horizon = int(line.replace('Time Horizon:', '').replace('days', '').strip())
                    signal['time_horizon'] = time_horizon
                except ValueError:
                    pass
        
        return signal
