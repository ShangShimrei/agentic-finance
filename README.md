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

A financial dashboard and trading platform powered by AI agents using the Model Context Protocol (MCP).

## Features

- React-based financial dashboard with real-time data visualization
- Agent-based trading strategies using MCP
- Technical, Fundamental, and Sentiment analysis
- Portfolio tracking and management
- Market overview and asset details

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git LFS (for handling large files)

### Installation

1. Clone the repository with Git LFS:
```
git lfs install
git clone <repository-url>
cd yrs-finance
```

2. Install Python dependencies:
```
pip install -r requirements.txt
```

3. Install React dashboard dependencies:
```
cd src/frontend/react-dashboard
npm install
cd ../../..
```

### Running the Application

Run the unified server that serves both the landing page and dashboard:

```
python run_app.py
```

The application will be available at:
- Landing page: http://localhost:8000
- Dashboard: http://localhost:8000/dashboard

### Development

To run the React dashboard in development mode:

```
cd src/frontend/react-dashboard
npm run dev
```

To build the React dashboard:

```
cd src/frontend/react-dashboard
npm run build
```

## Environment Variables

The application uses environment variables for configuration. Copy the sample files and modify as needed:

```
cp .env.example .env
cp src/frontend/react-dashboard/.env.example src/frontend/react-dashboard/.env
```

## Project Structure

- `src/agents/` - AI agent implementation with MCP
- `src/frontend/` - Web frontend code
  - `landing_page.html` - Static landing page
  - `react-dashboard/` - React dashboard application
  - `unified_server.py` - Server that serves both landing page and dashboard
- `run_app.py` - Main entry point to run the application

## Contributing

1. Use Git LFS for large binary files
2. Create a feature branch
3. Submit a pull request

## License

<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> aaf3d960 (First Commit: Project setup with README and basic structure)
=======
>>>>>>> 6d2f32db (First commit: Project setup with README, frontend dashboard and agent implementations)
=======
This project is licensed under the MIT License - see the LICENSE file for details.
>>>>>>> 33661dc4 (Implement full dashboard with multiple pages, unified server, and improved routing)
