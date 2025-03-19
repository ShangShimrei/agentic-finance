import logging
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Any, Optional
import datetime

logger = logging.getLogger(__name__)

class Visualizer:
    """
    Visualization component for the trading system.
    
    This component handles:
    - Agent signals visualization
    - Portfolio performance charts
    - Risk metrics visualization
    - Trading activity plots
    - Technical and sentiment indicators
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Visualizer with configuration settings.
        
        Args:
            config: Dictionary containing configuration settings
        """
        self.config = config
        self.name = "Trading System Visualizer"
        
        # Default chart settings
        self.chart_theme = config['visualization']['theme']
        self.default_height = config['visualization']['default_height']
        self.default_width = config['visualization']['default_width']
        
        logger.info(f"Initialized {self.name}")
    
    def plot_agent_signals(self, signals: Dict[str, Dict[str, Any]], 
                          symbol: str) -> go.Figure:
        """
        Create a visualization of agent trading signals for a symbol.
        
        Args:
            signals: Dictionary of agent signals
            symbol: Stock symbol
            
        Returns:
            Plotly figure object
        """
        # Extract agent names and confidence levels
        agents = []
        confidences = []
        actions = []
        
        for agent, signal in signals.items():
            if symbol in signal:
                agents.append(agent)
                confidences.append(signal[symbol]['confidence'])
                actions.append(signal[symbol]['action'])
        
        # Create color map for actions
        color_map = {
            'BUY': 'green',
            'SELL': 'red',
            'HOLD': 'gray'
        }
        colors = [color_map[action] for action in actions]
        
        # Create horizontal bar chart
        fig = go.Figure(data=[
            go.Bar(
                y=agents,
                x=confidences,
                orientation='h',
                marker_color=colors,
                text=[f"{conf:.2f}" for conf in confidences],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title=f"Agent Signals for {symbol}",
            xaxis_title="Confidence Level",
            yaxis_title="Agent",
            height=self.default_height,
            width=self.default_width,
            template=self.chart_theme
        )
        
        return fig
    
    def plot_portfolio_performance(self, performance_data: Dict[str, Any]) -> go.Figure:
        """
        Create portfolio performance visualization.
        
        Args:
            performance_data: Dictionary containing portfolio performance metrics
            
        Returns:
            Plotly figure object
        """
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add portfolio value line
        fig.add_trace(
            go.Scatter(
                x=performance_data['dates'],
                y=performance_data['portfolio_value'],
                name="Portfolio Value",
                line=dict(color="blue")
            ),
            secondary_y=False
        )
        
        # Add returns line
        fig.add_trace(
            go.Scatter(
                x=performance_data['dates'],
                y=performance_data['returns'],
                name="Returns (%)",
                line=dict(color="green")
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title="Portfolio Performance",
            height=self.default_height,
            width=self.default_width,
            template=self.chart_theme,
            hovermode="x unified"
        )
        
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Portfolio Value ($)", secondary_y=False)
        fig.update_yaxes(title_text="Returns (%)", secondary_y=True)
        
        return fig
    
    def plot_risk_metrics(self, risk_data: Dict[str, Any]) -> go.Figure:
        """
        Create risk metrics visualization.
        
        Args:
            risk_data: Dictionary containing risk metrics
            
        Returns:
            Plotly figure object
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Value at Risk (VaR)",
                "Position Sizes",
                "Risk Allocation",
                "Risk vs Return"
            )
        )
        
        # VaR over time
        fig.add_trace(
            go.Scatter(
                x=risk_data['dates'],
                y=risk_data['var'],
                name="VaR",
                line=dict(color="red")
            ),
            row=1, col=1
        )
        
        # Position sizes
        fig.add_trace(
            go.Bar(
                x=risk_data['symbols'],
                y=risk_data['position_sizes'],
                name="Position Size",
                marker_color="blue"
            ),
            row=1, col=2
        )
        
        # Risk allocation pie chart
        fig.add_trace(
            go.Pie(
                labels=risk_data['categories'],
                values=risk_data['risk_allocation'],
                name="Risk Allocation"
            ),
            row=2, col=1
        )
        
        # Risk vs Return scatter
        fig.add_trace(
            go.Scatter(
                x=risk_data['volatility'],
                y=risk_data['returns'],
                mode='markers+text',
                text=risk_data['symbols'],
                textposition="top center",
                name="Risk/Return"
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=self.default_height * 2,
            width=self.default_width * 2,
            template=self.chart_theme,
            showlegend=False
        )
        
        return fig
    
    def plot_trading_activity(self, trades: List[Dict[str, Any]]) -> go.Figure:
        """
        Create trading activity visualization.
        
        Args:
            trades: List of trade dictionaries
            
        Returns:
            Plotly figure object
        """
        # Convert trades to DataFrame
        df = pd.DataFrame(trades)
        
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add trade markers
        fig.add_trace(
            go.Scatter(
                x=df[df['action'] == 'BUY']['timestamp'],
                y=df[df['action'] == 'BUY']['price'],
                mode='markers',
                name='Buy',
                marker=dict(
                    symbol='triangle-up',
                    size=10,
                    color='green'
                )
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=df[df['action'] == 'SELL']['timestamp'],
                y=df[df['action'] == 'SELL']['price'],
                mode='markers',
                name='Sell',
                marker=dict(
                    symbol='triangle-down',
                    size=10,
                    color='red'
                )
            )
        )
        
        # Add volume bars
        fig.add_trace(
            go.Bar(
                x=df['timestamp'],
                y=df['volume'],
                name="Volume",
                marker_color='lightgray',
                opacity=0.3
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title="Trading Activity",
            height=self.default_height,
            width=self.default_width,
            template=self.chart_theme
        )
        
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Price", secondary_y=False)
        fig.update_yaxes(title_text="Volume", secondary_y=True)
        
        return fig
    
    def plot_technical_indicators(self, technical_data: Dict[str, Any],
                                symbol: str) -> go.Figure:
        """
        Create technical indicators visualization.
        
        Args:
            technical_data: Dictionary containing technical indicators
            symbol: Stock symbol
            
        Returns:
            Plotly figure object
        """
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(
                f"{symbol} Price and Moving Averages",
                "RSI",
                "MACD"
            )
        )
        
        # Price and moving averages
        fig.add_trace(
            go.Candlestick(
                x=technical_data['dates'],
                open=technical_data['open'],
                high=technical_data['high'],
                low=technical_data['low'],
                close=technical_data['close'],
                name="Price"
            ),
            row=1, col=1
        )
        
        for ma in ['MA20', 'MA50', 'MA200']:
            fig.add_trace(
                go.Scatter(
                    x=technical_data['dates'],
                    y=technical_data[ma.lower()],
                    name=ma,
                    line=dict(width=1)
                ),
                row=1, col=1
            )
        
        # RSI
        fig.add_trace(
            go.Scatter(
                x=technical_data['dates'],
                y=technical_data['rsi'],
                name="RSI",
                line=dict(color="purple")
            ),
            row=2, col=1
        )
        
        # Add RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        fig.add_trace(
            go.Scatter(
                x=technical_data['dates'],
                y=technical_data['macd'],
                name="MACD",
                line=dict(color="blue")
            ),
            row=3, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=technical_data['dates'],
                y=technical_data['macd_signal'],
                name="Signal",
                line=dict(color="orange")
            ),
            row=3, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=technical_data['dates'],
                y=technical_data['macd_hist'],
                name="Histogram",
                marker_color="gray"
            ),
            row=3, col=1
        )
        
        fig.update_layout(
            height=self.default_height * 2,
            width=self.default_width,
            template=self.chart_theme,
            xaxis3_title="Date",
            yaxis_title="Price",
            yaxis2_title="RSI",
            yaxis3_title="MACD"
        )
        
        return fig
    
    def plot_sentiment_analysis(self, sentiment_data: Dict[str, Any],
                              symbol: str) -> go.Figure:
        """
        Create sentiment analysis visualization.
        
        Args:
            sentiment_data: Dictionary containing sentiment metrics
            symbol: Stock symbol
            
        Returns:
            Plotly figure object
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Overall Sentiment",
                "News vs Social Sentiment",
                "Volume Analysis",
                "Sentiment Distribution"
            )
        )
        
        # Overall sentiment trend
        fig.add_trace(
            go.Scatter(
                x=sentiment_data['dates'],
                y=sentiment_data['overall_sentiment'],
                name="Overall",
                line=dict(color="blue")
            ),
            row=1, col=1
        )
        
        # News vs Social sentiment
        fig.add_trace(
            go.Scatter(
                x=sentiment_data['dates'],
                y=sentiment_data['news_sentiment'],
                name="News",
                line=dict(color="green")
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=sentiment_data['dates'],
                y=sentiment_data['social_sentiment'],
                name="Social",
                line=dict(color="orange")
            ),
            row=1, col=2
        )
        
        # Volume analysis
        fig.add_trace(
            go.Bar(
                x=sentiment_data['dates'],
                y=sentiment_data['volume'],
                name="Volume",
                marker_color="lightgray"
            ),
            row=2, col=1
        )
        
        # Sentiment distribution
        fig.add_trace(
            go.Histogram(
                x=sentiment_data['sentiment_scores'],
                name="Distribution",
                nbinsx=20,
                marker_color="purple"
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=self.default_height * 2,
            width=self.default_width * 2,
            template=self.chart_theme,
            title=f"Sentiment Analysis for {symbol}"
        )
        
        return fig
