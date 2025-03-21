"""
Web dashboard for the trading platform that displays real-time data and performance metrics.
"""
import logging
import json
import os
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import threading
import http.server
import socketserver
import webbrowser

logger = logging.getLogger(__name__)

# HTML template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic Hedge Fund Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background-color: #2c3e50;
            color: white;
            padding: 15px 0;
            text-align: center;
        }
        h1 {
            margin: 0;
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        .card h2 {
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .metrics {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        .metric {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            margin: 5px 0;
            color: #2980b9;
        }
        .metric-label {
            font-size: 14px;
            color: #7f8c8d;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .buy {
            color: green;
            font-weight: bold;
        }
        .sell {
            color: red;
            font-weight: bold;
        }
        .hold {
            color: gray;
        }
        .success {
            color: green;
        }
        .failed {
            color: red;
        }
        .loader {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 2s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .full-width {
            grid-column: 1 / -1;
        }
        #refresh-btn {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }
        #refresh-btn:hover {
            background-color: #2980b9;
        }
        .timestamp {
            font-size: 12px;
            color: #7f8c8d;
            text-align: right;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Agentic Hedge Fund Dashboard</h1>
        </div>
    </header>
    
    <div class="container">
        <div id="portfolio-summary" class="card">
            <h2>Portfolio Summary</h2>
            <div id="portfolio-metrics" class="metrics">
                <div class="metric">
                    <div class="metric-label">Total Value</div>
                    <div id="total-value" class="metric-value">$0.00</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Cash</div>
                    <div id="cash-value" class="metric-value">$0.00</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Today's Return</div>
                    <div id="daily-return" class="metric-value">0.00%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Total Return</div>
                    <div id="total-return" class="metric-value">0.00%</div>
                </div>
            </div>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h2>Current Positions</h2>
                <div id="positions-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Ticker</th>
                                <th>Quantity</th>
                                <th>Avg Price</th>
                                <th>Current Price</th>
                                <th>Value</th>
                                <th>Return</th>
                            </tr>
                        </thead>
                        <tbody id="positions-body">
                            <tr>
                                <td colspan="6" style="text-align: center;">No positions yet</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="card">
                <h2>Recent Trades</h2>
                <div id="trades-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Ticker</th>
                                <th>Action</th>
                                <th>Quantity</th>
                                <th>Price</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody id="trades-body">
                            <tr>
                                <td colspan="6" style="text-align: center;">No trades yet</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="card full-width">
                <h2>Agent Signals</h2>
                <div id="signals-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Agent</th>
                                <th>Ticker</th>
                                <th>Action</th>
                                <th>Confidence</th>
                                <th>Rationale</th>
                                <th>Time Horizon</th>
                            </tr>
                        </thead>
                        <tbody id="signals-body">
                            <tr>
                                <td colspan="6" style="text-align: center;">No signals yet</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <button id="refresh-btn" onclick="refreshData()">Refresh Data</button>
        <div class="timestamp">Last updated: <span id="last-updated">Never</span></div>
    </div>
    
    <script>
        // Function to fetch the latest data
        function refreshData() {
            fetch('/api/dashboard-data')
                .then(response => response.json())
                .then(data => {
                    updatePortfolioSummary(data.portfolio);
                    updatePositionsTable(data.portfolio.positions);
                    updateTradesTable(data.recent_trades);
                    updateSignalsTable(data.latest_signals);
                    document.getElementById('last-updated').textContent = new Date().toLocaleString();
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        }
        
        // Update portfolio summary metrics
        function updatePortfolioSummary(portfolio) {
            document.getElementById('total-value').textContent = '$' + portfolio.total_value.toLocaleString();
            document.getElementById('cash-value').textContent = '$' + portfolio.cash.toLocaleString();
            document.getElementById('daily-return').textContent = portfolio.daily_return.toFixed(2) + '%';
            document.getElementById('total-return').textContent = portfolio.total_return.toFixed(2) + '%';
            
            // Add color to return values
            const dailyReturn = document.getElementById('daily-return');
            const totalReturn = document.getElementById('total-return');
            
            dailyReturn.style.color = portfolio.daily_return >= 0 ? 'green' : 'red';
            totalReturn.style.color = portfolio.total_return >= 0 ? 'green' : 'red';
        }
        
        // Update positions table
        function updatePositionsTable(positions) {
            const tableBody = document.getElementById('positions-body');
            tableBody.innerHTML = '';
            
            if (Object.keys(positions).length === 0) {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="6" style="text-align: center;">No positions yet</td>';
                tableBody.appendChild(row);
                return;
            }
            
            for (const ticker in positions) {
                const position = positions[ticker];
                const row = document.createElement('tr');
                
                const currentValue = position.quantity * position.last_price;
                const costBasis = position.quantity * position.avg_price;
                const returnPct = ((position.last_price / position.avg_price) - 1) * 100;
                
                row.innerHTML = `
                    <td>${ticker}</td>
                    <td>${position.quantity}</td>
                    <td>$${position.avg_price.toFixed(2)}</td>
                    <td>$${position.last_price.toFixed(2)}</td>
                    <td>$${currentValue.toFixed(2)}</td>
                    <td style="color: ${returnPct >= 0 ? 'green' : 'red'}">${returnPct.toFixed(2)}%</td>
                `;
                
                tableBody.appendChild(row);
            }
        }
        
        // Update trades table
        function updateTradesTable(trades) {
            const tableBody = document.getElementById('trades-body');
            tableBody.innerHTML = '';
            
            if (trades.length === 0) {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="6" style="text-align: center;">No trades yet</td>';
                tableBody.appendChild(row);
                return;
            }
            
            for (const trade of trades) {
                const row = document.createElement('tr');
                const date = new Date(trade.executed_at || trade.submitted_at).toLocaleString();
                
                row.innerHTML = `
                    <td>${date}</td>
                    <td>${trade.ticker}</td>
                    <td class="${trade.action.toLowerCase()}">${trade.action}</td>
                    <td>${trade.quantity}</td>
                    <td>$${trade.average_price ? trade.average_price.toFixed(2) : '-'}</td>
                    <td class="${trade.status.toLowerCase() === 'filled' ? 'success' : trade.status.toLowerCase() === 'rejected' ? 'failed' : ''}">${trade.status}</td>
                `;
                
                tableBody.appendChild(row);
            }
        }
        
        // Update signals table
        function updateSignalsTable(signals) {
            const tableBody = document.getElementById('signals-body');
            tableBody.innerHTML = '';
            
            if (signals.length === 0) {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="6" style="text-align: center;">No signals yet</td>';
                tableBody.appendChild(row);
                return;
            }
            
            for (const signal of signals) {
                const row = document.createElement('tr');
                
                row.innerHTML = `
                    <td>${signal.agent}</td>
                    <td>${signal.ticker}</td>
                    <td class="${signal.action.toLowerCase()}">${signal.action}</td>
                    <td>${(signal.confidence * 100).toFixed(0)}%</td>
                    <td>${signal.rationale}</td>
                    <td>${signal.time_horizon || 'N/A'}</td>
                `;
                
                tableBody.appendChild(row);
            }
        }
        
        // Initial data load
        document.addEventListener('DOMContentLoaded', function() {
            refreshData();
            // Auto-refresh every 60 seconds
            setInterval(refreshData, 60000);
        });
    </script>
</body>
</html>
"""

class DashboardData:
    """
    Class to store and manage dashboard data.
    """
    def __init__(self):
        """Initialize empty dashboard data."""
        self.portfolio = {
            "cash": 100000.0,
            "positions": {},
            "total_value": 100000.0,
            "daily_return": 0.0,
            "total_return": 0.0,
            "initial_capital": 100000.0
        }
        self.recent_trades = []
        self.latest_signals = []
        self.last_updated = datetime.now().isoformat()
    
    def update_portfolio(self, portfolio_data: Dict[str, Any]) -> None:
        """
        Update portfolio data.
        
        Args:
            portfolio_data: New portfolio data
        """
        self.portfolio = portfolio_data
        self.last_updated = datetime.now().isoformat()
    
    def update_trades(self, trades_data: List[Dict[str, Any]]) -> None:
        """
        Update recent trades data.
        
        Args:
            trades_data: New trades data
        """
        self.recent_trades = trades_data
        self.last_updated = datetime.now().isoformat()
    
    def update_signals(self, signals_data: List[Dict[str, Any]]) -> None:
        """
        Update latest signals data.
        
        Args:
            signals_data: New signals data
        """
        self.latest_signals = signals_data
        self.last_updated = datetime.now().isoformat()
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get all dashboard data.
        
        Returns:
            Dictionary with all dashboard data
        """
        return {
            "portfolio": self.portfolio,
            "recent_trades": self.recent_trades,
            "latest_signals": self.latest_signals,
            "last_updated": self.last_updated
        }
    
    def to_json(self) -> str:
        """
        Convert dashboard data to JSON string.
        
        Returns:
            JSON string representation of dashboard data
        """
        return json.dumps(self.get_dashboard_data())

class DashboardRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for the dashboard server."""
    
    # Reference to the dashboard data object
    dashboard_data = None
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode())
        elif self.path == '/api/dashboard-data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if self.dashboard_data:
                self.wfile.write(self.dashboard_data.to_json().encode())
            else:
                self.wfile.write(json.dumps({"error": "No data available"}).encode())
        else:
            self.send_error(404)

class TradingDashboard:
    """
    Web dashboard for displaying trading system information and performance metrics.
    """
    
    def __init__(self, host: str = 'localhost', port: int = 8080):
        """
        Initialize the trading dashboard.
        
        Args:
            host: Host address to bind the server
            port: Port to use for the server
        """
        self.host = host
        self.port = port
        self.server = None
        self.server_thread = None
        self.dashboard_data = DashboardData()
        
        # Set the dashboard data in the request handler
        DashboardRequestHandler.dashboard_data = self.dashboard_data
        
        logger.info(f"Initializing Trading Dashboard on {host}:{port}")
    
    def start(self) -> None:
        """Start the dashboard web server."""
        try:
            # Create a server and bind to specified host and port
            self.server = socketserver.TCPServer((self.host, self.port), DashboardRequestHandler)
            
            # Start the server in a separate thread
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            logger.info(f"Dashboard server started at http://{self.host}:{self.port}")
            logger.info(f"Open a browser and navigate to http://{self.host}:{self.port} to view the dashboard")
            
            # Open the dashboard in the default web browser
            webbrowser.open(f"http://{self.host}:{self.port}")
            
        except Exception as e:
            logger.error(f"Error starting dashboard server: {e}")
            raise
    
    def stop(self) -> None:
        """Stop the dashboard web server."""
        if self.server:
            self.server.shutdown()
            self.server = None
            logger.info("Dashboard server stopped")
    
    def update_portfolio(self, portfolio_data: Dict[str, Any]) -> None:
        """
        Update portfolio information displayed on the dashboard.
        
        Args:
            portfolio_data: Updated portfolio data
        """
        self.dashboard_data.update_portfolio(portfolio_data)
        logger.debug("Dashboard portfolio data updated")
    
    def update_trades(self, trades_data: List[Dict[str, Any]]) -> None:
        """
        Update recent trades displayed on the dashboard.
        
        Args:
            trades_data: Recent trade data
        """
        self.dashboard_data.update_trades(trades_data)
        logger.debug("Dashboard trades data updated")
    
    def update_signals(self, signals_data: List[Dict[str, Any]]) -> None:
        """
        Update agent signals displayed on the dashboard.
        
        Args:
            signals_data: Latest agent signals
        """
        self.dashboard_data.update_signals(signals_data)
        logger.debug("Dashboard signals data updated")
    
    def update_all(self, 
                  portfolio_data: Optional[Dict[str, Any]] = None,
                  trades_data: Optional[List[Dict[str, Any]]] = None,
                  signals_data: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Update all dashboard data at once.
        
        Args:
            portfolio_data: Updated portfolio data
            trades_data: Recent trade data
            signals_data: Latest agent signals
        """
        if portfolio_data:
            self.dashboard_data.update_portfolio(portfolio_data)
        
        if trades_data:
            self.dashboard_data.update_trades(trades_data)
        
        if signals_data:
            self.dashboard_data.update_signals(signals_data)
        
        logger.debug("All dashboard data updated")
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get current dashboard data.
        
        Returns:
            Dictionary with all dashboard data
        """
        return self.dashboard_data.get_dashboard_data() 