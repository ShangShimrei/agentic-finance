<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
﻿# Agentic Finance

A modern AI-powered trading platform that combines multiple trading agents to make intelligent investment decisions.

## 🚀 Features

- **Multi-Agent Trading System**
  - Buffet Agent (Value Investing)
  - Ackman Agent (Activist Investing)
  - Technical Agent (Technical Analysis)
  - Sentiment Agent (Market Sentiment)
  - Fundamental Agent (Fundamental Analysis)
  - Research Agent (Deep Research)

- **Modern Dashboard**
  - Real-time portfolio tracking
  - Performance analytics
  - Agent signal visualization
  - Recent activity feed
  - Dark mode interface

- **Advanced Analytics**
  - Portfolio performance tracking
  - Win rate analysis
  - Multi-timeframe analysis
  - Risk metrics

## 🛠️ Tech Stack

- **Frontend**
  - React with TypeScript
  - Tailwind CSS for styling
  - Plotly.js for charts
  - Real-time data updates

- **Backend**
  - Python
  - FastAPI
  - Machine Learning models
  - Real-time data processing

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agentic-finance.git
   cd agentic-finance
   ```

2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd src/frontend
   npm install
   ```

4. Set up environment variables:
   - Create `.env` file in `src/frontend` with:
     ```
     REACT_APP_API_URL=http://localhost:5000/api
     BROWSER=none
     ```

## 🚀 Running the Application

1. Start the backend server:
   ```bash
   # From project root
   python src/main.py
   ```

2. Start the frontend development server:
   ```bash
   # From src/frontend directory
   npm start
   ```

3. Access the application at `http://localhost:3000`

## 📊 Trading Agents

### Buffet Agent
Implements value investing strategies inspired by Warren Buffet's principles.

### Ackman Agent
Focuses on activist investing opportunities and special situations.

### Technical Agent
Analyzes price action, technical indicators, and chart patterns.

### Sentiment Agent
Processes market sentiment from news and social media.

### Fundamental Agent
Analyzes company financials and economic indicators.

### Research Agent
Conducts deep research on companies and market trends.

## 🔒 Security

- Secure API endpoints
- Environment variable configuration
- Safe handling of trading signals

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Trading algorithms inspired by successful investors
- Modern UI/UX design principles
- Open-source community contributions

---
Built with ❤️ for algorithmic trading

=======
=======
>>>>>>> 6d2f32db (First commit: Project setup with README, frontend dashboard and agent implementations)
﻿# Agentic Finance
=======
# YRS Agentic Finance Platform
>>>>>>> 33661dc4 (Implement full dashboard with multiple pages, unified server, and improved routing)

A comprehensive financial platform powered by AI agents for trading and portfolio management.

## Quick Start

Run the application with a single command:

```bash
# Using Python
python run_app.py

# OR using npm
npm start
```

This will start the unified server and open the application in your default browser.

## Features

- **Landing Page**: Introduction to the platform features
- **Dashboard**: Comprehensive trading and portfolio management
  - Portfolio overview with time period selection
  - Multiple chart types (line, candlestick)
  - Market overview
  - Asset allocation breakdown
  - Recent transactions

## Architecture

The application consists of:

1. **Frontend**
   - Landing page (static HTML)
   - React dashboard (interactive SPA)
   - Unified server (serves both components from a single port)

2. **Backend**
   - Trading agents using the Model Context Protocol (MCP)
   - Data processing and analysis tools
   - Portfolio management system

## Development

### Prerequisites

- Python 3.7+
- Node.js 14+
- npm 6+

### Running in Development Mode

The unified server automatically starts both the landing page and the React dashboard in development mode, with hot reloading enabled for the React components.

```bash
# Run the unified server
npm start

# OR run just the dashboard in development mode
npm run dev:dashboard
```

### Building for Production

To build the application for production:

```bash
# Build the React dashboard
npm run build:dashboard

# Then run the unified server
npm start
```

## Troubleshooting

If you encounter issues:

1. Make sure you have all dependencies installed:
   ```bash
   cd src/frontend/react-dashboard
   npm install
   ```

2. Check that port 8000 is available (the unified server uses this port)

3. If the React dashboard doesn't load, try building it manually:
   ```bash
   npm run build:dashboard
   ```

4. For detailed logs, check the console output when running the server

## Overview

The YRS Agentic Finance Platform is a modern trading platform that utilizes multiple specialized agents to analyze markets and make trading decisions. These agents communicate using the Model Context Protocol, allowing them to share insights and collaborate on decisions.

### Backend Features

- **Model Context Protocol Integration**: Agents communicate through MCP, enabling seamless collaboration
- **Multiple Specialized Agents**:
  - Technical Analysis Agent: Analyzes price patterns and technical indicators
  - Fundamental Analysis Agent: Evaluates financial metrics and company fundamentals
  - Sentiment Analysis Agent: Monitors news and social media sentiment
- **Agent Orchestration**: A central orchestrator manages the agents and combines their signals

### Directory Structure

```
src/
├── agents/                   # Agent modules
│   ├── __init__.py           # Agent module exports
│   ├── base_agent.py         # Base agent class with MCP integration
│   ├── mcp_tools.py          # Tools registered with MCP server
│   └── trading/              # Trading agent implementations
│       ├── technical_agent.py    # Technical analysis agent
│       ├── fundamental_agent.py  # Fundamental analysis agent
│       └── sentiment_agent.py    # Sentiment analysis agent
├── frontend/                 # Frontend code
│   ├── landing_page.html     # Landing page
│   ├── unified_server.py     # Unified server for both components
│   └── react-dashboard/      # React dashboard application
│       └── ...
├── start_mcp_server.py       # Script to start the MCP server
├── run_technical_agent.py    # Script to run the Technical agent
├── run_fundamental_agent.py  # Script to run the Fundamental agent
├── run_sentiment_agent.py    # Script to run the Sentiment agent
└── run_agent_orchestrator.py # Script to orchestrate the agents
```

## Agent Communication with MCP

The Model Context Protocol (MCP) enables agents to communicate by:

1. Registering tools that agents can use
2. Allowing agents to share context and insights
3. Facilitating message passing between agents
4. Maintaining a shared state for agent coordination

For example, when the Technical Agent identifies a potential trading signal:

```python
# The Technical Agent can call tools registered with the MCP server
market_data = agent.call_tool("fetch_market_data", ticker="AAPL")
indicators = agent.call_tool("calculate_indicators", data=market_data)

# And share insights with other agents
agent.send_message(
    "Identified bullish pattern for AAPL with RSI oversold",
    recipients=["Fundamental Analysis Agent", "Sentiment Analysis Agent"]
)
```

## Advanced Configuration

You can customize the behavior of agents through command-line arguments:

```bash
python src/run_technical_agent.py --tickers AAPL MSFT GOOGL --interval 300
python src/run_fundamental_agent.py --tickers AAPL MSFT GOOGL --interval 3600
python src/run_sentiment_agent.py --tickers AAPL MSFT GOOGL --interval 1800
```

## License

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> aaf3d960 (First Commit: Project setup with README and basic structure)
=======
>>>>>>> 6d2f32db (First commit: Project setup with README, frontend dashboard and agent implementations)
=======
This project is licensed under the MIT License - see the LICENSE file for details.
>>>>>>> 33661dc4 (Implement full dashboard with multiple pages, unified server, and improved routing)
=======
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This platform is for demonstration purposes only. The trading signals generated are not financial advice.
>>>>>>> fe1ded8a (commit for initial working UI)
