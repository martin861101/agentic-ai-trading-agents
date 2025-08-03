from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict
import asyncio
import logging
import json
from datetime import datetime
import sys
import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# LangGraph MCP pipeline
from orchestrator.mcp_graph import run_mcp_pipeline

# DB Setup
DATABASE_URL = "postgresql://postgres:password@postgres:5432/agentic_trading"
engine = create_engine(DATABASE_URL)
max_retries = 10
for attempt in range(1, max_retries + 1):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅  Connected to PostgreSQL!")
        break
    except OperationalError as e:
        print(f"⏳  Attempt {attempt}: Postgres not ready yet: {e}")
        time.sleep(3)
else:
    raise Exception("❌ Could not connect to Postgres after 10 attempts")

from db.db_session import get_db, init_db
from db.models import TradeSignal, Agent, TradeOutcome
from .event_bus import event_bus
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agentic Trading Orchestrator",
    description="Central orchestrator for AI trading agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.copy():
            try:
                await connection.send_json(message)
            except:
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    try:
        init_db()
        await event_bus.connect()
        asyncio.create_task(event_bus.start_listening())
        logger.info("✅ Orchestrator started successfully")
    except Exception as e:
        logger.error(f"❌ Failed to start orchestrator: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    try:
        await event_bus.disconnect()
    except:
        pass
    logger.info("🛑 Orchestrator shut down")

# --- API Routes ---

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/agents")
async def get_agents():
    agents = [
        {"name": "chartanalyst", "status": "active", "port": 8001},
        {"name": "riskmanager", "status": "active", "port": 8002},
        {"name": "marketsentinel", "status": "active", "port": 8003},
        {"name": "macroforecaster", "status": "active", "port": 8004},
        {"name": "tacticbot", "status": "active", "port": 8005},
        {"name": "platformpilot", "status": "active", "port": 8006},
    ]
    return agents

@app.get("/signals")
async def get_recent_signals(limit: int = 50):
    signals = [
        {
            "symbol": "EURUSD",
            "signal_type": "BUY",
            "confidence": 0.85,
            "agent_name": "chartanalyst",
            "timestamp": datetime.now().isoformat(),
            "reasoning": "Strong bullish pattern detected"
        }
    ]
    return signals

@app.post("/manual_signal")
async def create_manual_signal(signal_data: Dict):
    try:
        await manager.broadcast({
            "type": "manual_signal",
            "data": signal_data
        })
        return {"status": "success", "message": "Manual signal created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from pydantic import BaseModel

class MCPRequest(BaseModel):
    symbol: str
    timeframe: str

@app.post("/run_mcp")
async def run_mcp_endpoint(payload: MCPRequest):
    try:
        result = await run_mcp_pipeline(symbol=payload.symbol, timeframe=payload.timeframe)
        return result
    except Exception as e:
        logger.error(f"Error running MCP: {e}")
        raise HTTPException(status_code=500, detail="MCP execution failed")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.orchestrator_port)
