from fastapi import FastAPI, HTTPException
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

def create_api(
    agents: Dict[str, Any],
    risk_manager: Any,
    portfolio_manager: Any,
    execution_engine: Any,
    visualizer: Any,
    research_agent: Any,
    config: Dict[str, Any]
) -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Args:
        agents: Dictionary of trading agents
        risk_manager: Risk Manager instance
        portfolio_manager: Portfolio Manager instance
        execution_engine: Execution Engine instance
        visualizer: Visualizer instance
        research_agent: Research Agent instance
        config: Configuration dictionary
        
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="Agentic Finance API",
        description="API for the Agentic Finance multi-agent trading system",
        version="0.1.0"
    )
    
    # Store components in app state
    app.state.agents = agents
    app.state.risk_manager = risk_manager
    app.state.portfolio_manager = portfolio_manager
    app.state.execution_engine = execution_engine
    app.state.visualizer = visualizer
    app.state.research_agent = research_agent
    app.state.config = config
    
    @app.get("/")
    async def root():
        """Root endpoint returning basic system information."""
        return {
            "name": "Agentic Finance API",
            "version": "0.1.0",
            "status": "running",
            "active_agents": list(agents.keys())
        }
    
    @app.get("/agents")
    async def list_agents():
        """List all active trading agents."""
        return {
            "agents": [
                {
                    "name": name,
                    "type": agent.__class__.__name__,
                    "weight": agent.weight
                }
                for name, agent in app.state.agents.items()
            ]
        }
    
    @app.get("/signals/{symbol}")
    async def get_signals(symbol: str):
        """
        Get trading signals for a specific symbol.
        
        Args:
            symbol: Stock symbol to analyze
        """
        try:
            # Get signals from each agent
            signals = {}
            for name, agent in app.state.agents.items():
                signals[name] = agent.generate_signal([symbol])[symbol]
            
            # Process through risk manager
            risk_adjusted_signals = app.state.risk_manager.process_signals(
                {name: {symbol: signal} for name, signal in signals.items()}
            )
            
            return {
                "symbol": symbol,
                "raw_signals": signals,
                "risk_adjusted_signals": risk_adjusted_signals
            }
        except Exception as e:
            logger.error(f"Error generating signals for {symbol}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/portfolio")
    async def get_portfolio():
        """Get current portfolio state."""
        try:
            return app.state.portfolio_manager.get_portfolio_state()
        except Exception as e:
            logger.error(f"Error getting portfolio state: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/orders")
    async def get_orders(limit: int = 100):
        """
        Get order history.
        
        Args:
            limit: Maximum number of orders to return
        """
        try:
            return {
                "orders": app.state.execution_engine.get_order_history(limit=limit)
            }
        except Exception as e:
            logger.error(f"Error getting order history: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/trade/{symbol}")
    async def execute_trade(symbol: str, action: str, size: float):
        """
        Execute a trade for a specific symbol.
        
        Args:
            symbol: Stock symbol to trade
            action: Trade action (BUY, SELL, SHORT, COVER)
            size: Position size as percentage of portfolio
        """
        try:
            # Validate action
            if action not in ['BUY', 'SELL', 'SHORT', 'COVER']:
                raise ValueError(f"Invalid action: {action}")
            
            # Create portfolio action
            portfolio_action = {
                symbol: {
                    'action': action,
                    'size': size,
                    'reason': f"Manual trade execution: {action} {size:.1%} of {symbol}",
                    'signal_confidence': 1.0,  # Manual trades have full confidence
                    'signal_reasoning': ["Manual trade execution"]
                }
            }
            
            # Execute the trade
            result = app.state.execution_engine.execute_actions(portfolio_action)
            
            # If successful, update portfolio
            if result[symbol]['status'] == 'filled':
                app.state.portfolio_manager.update_position(
                    symbol=symbol,
                    quantity=result[symbol]['quantity'],
                    price=result[symbol]['price'],
                    action=action
                )
            
            return result
        except Exception as e:
            logger.error(f"Error executing trade for {symbol}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/research")
    async def get_research():
        """Get research insights from the Research Agent."""
        try:
            # Get portfolio state
            portfolio_state = app.state.portfolio_manager.get_portfolio_state()
            
            # Get recent orders
            recent_orders = app.state.execution_engine.get_order_history(limit=50)
            
            # Generate research insights
            insights = app.state.research_agent.analyze_portfolio(
                portfolio_state=portfolio_state,
                recent_orders=recent_orders
            )
            
            return {
                "insights": insights,
                "timestamp": insights.get('timestamp')
            }
        except Exception as e:
            logger.error(f"Error generating research insights: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/market-data/{symbol}")
    async def get_market_data(symbol: str):
        """
        Get current market data for a symbol.
        
        Args:
            symbol: Stock symbol
        """
        try:
            price = app.state.execution_engine.get_market_price(symbol)
            if price is None:
                raise ValueError(f"No market data available for {symbol}")
            
            return {
                "symbol": symbol,
                "price": price,
                "timestamp": app.state.execution_engine.market_prices.get(symbol)
            }
        except Exception as e:
            logger.error(f"Error getting market data for {symbol}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return app
