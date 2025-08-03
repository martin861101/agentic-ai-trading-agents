### 📈 Agentic AI Trading System (LangGraph Orchestrated)

This project implements an **Agentic AI stock trading system**, built with a modular multi-agent architecture orchestrated using [LangGraph](https://github.com/langchain-ai/langgraph). Each agent contributes specialized reasoning using LLMs such as **Mistral**, **LLaMA**, and APIs like **Tavily** or **Selenium** for real-world visibility.

---

### ⚙️ Architecture Overview

```
               ┌──────────────────────┐
               │   Frontend    │
               │   (React)     │
               └─────┌────────┘
                      │
               ┌─────│─────────┐
               │  Orchestrator │ <──── REST & WebSocket API (FastAPI)
               │ (LangGraph)   │
               └────│────────┘
                    │
        ┌─────────┬────────────────────────────┐
        ▼           ▼                       ▼
   chart_analyst   risk_manager      market_sentinel
     (LLMs +         (logic +             (news/
   chart data)      thresholds)       event scanner)

                      ...
        (additional agents plugged into LangGraph)

```

---

### 🧠 Agents Overview

Each agent lives in `backend/agents/<agent_name>/`, and uses:

* **LLMs (Mistral/LLaMA via OpenRouter)** for reasoning
* **Tavily API** or **Selenium** for real-time intelligence
* **Shared Event Bus (Redis)** for coordination
* **Postgres DB** to persist signals and outcomes

---

### 🚀 Quickstart

#### 1. Clone the repository

```bash
git clone https://github.com/your-org/agentic-ai-trading-system.git
cd agentic-ai-trading-system/agentic-trading
```

#### 2. Fill in `.env` (already present)

Ensure your `.env` has valid API keys:

```
OPENROUTER_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
DATABASE_URL=postgresql://postgres:password@postgres:5432/agentic_trading
...
```

#### 3. Build and run with Docker Compose

```bash
docker-compose up -d --build
```

Access services:

* **API Docs**: [http://localhost:8007/docs](http://localhost:8007/docs)
* **Frontend UI**: [http://localhost:3000](http://localhost:3000)

#### 4. Run the MCP (Multi-Agent Control Protocol)

```bash
curl -X POST http://localhost:8007/run_mcp \
  -H "Content-Type: application/json" \
  -d '{"symbol": "EURUSD", "timeframe": "1h"}'
```

---

### 🔪 Testing a Single Agent (e.g. `chart_analyst`)

```bash
cd backend
python3 -m agents.chartanalyst.test
```

Make sure `__init__.py` files are present in all relevant folders.

---

### 📙 LangGraph MCP Setup

The orchestration graph is defined in:

```
backend/orchestrator/mcp_graph.py
```

It uses LangGraph’s `StateGraph` to build the reasoning flow across agents. You can visualize or extend the graph from here.

---

### 📂 Project Structure

```
agentic-trading/
├── backend/
│   ├── agents/                # Individual agent folders
│   ├── db/                    # DB models and init
│   └── orchestrator/
│       ├── api.py             # FastAPI orchestrator
│       ├── mcp_graph.py       # LangGraph setup
│       └── event_bus.py       # Redis PubSub
└── frontend/                  # React UI (built with react-scripts)

+ .env, docker-compose.yml, etc.
```

---

### 🛠️ Tech Stack

* **LangGraph** for agent graph orchestration
* **FastAPI** + **Uvicorn** for REST + WebSocket
* **React** for dashboard
* **PostgreSQL** as primary DB
* **Redis** for event messaging
* **OpenRouter LLMs** (Mistral, LLaMA, etc.)
* **Tavily / Selenium** for external visibility

---

### 📊 Coming Soon

* ✅ Graph visualization endpoint
* ✅ Per-agent logs and trace UI
* ⟳ Retraining agents on feedback
* 📈 Agent performance dashboards
* 🧠 Auto-improving agents using outcomes

---

### 🧠 License & Credits

MIT Licensed. Powered by:

* [LangGraph](https://github.com/langchain-ai/langgraph)
* [Mistral via OpenRouter](https://openrouter.ai/)
* [Tavily Search](https://www.tavily.com/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Docker](https://www.docker.com/)
