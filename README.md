# Agentic AI Trading System

A modular, microservices-based AI trading system with specialized agents for different aspects of trading analysis and execution.

## Architecture

- **ChartAnalyst**: Pattern recognition and technical analysis
- **RiskManager**: Position sizing and risk assessment  
- **MarketSentinel**: Volatility monitoring and scalping opportunities
- **MacroForecaster**: News analysis and macro event impact
- **TacticBot**: Trade execution logic and timing
- **PlatformPilot**: Platform automation and logging

## Quick Start

1. Copy environment file: `cp .env.example .env`
2. Update API keys in `.env`
3. Run: `docker-compose up -d`
4. Access dashboard: http://localhost:3000
5. API documentation: http://localhost:8000/docs

## Development

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn orchestrator.api:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Features

- Real-time WebSocket communication
- Event-driven agent coordination
- Comprehensive logging and analytics
- Modern React dashboard with TradingView integration
- Docker containerization
- PostgreSQL database with TimescaleDB extensions
