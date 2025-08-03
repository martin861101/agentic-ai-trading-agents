from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
import asyncio
import httpx
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Marketsentinel Agent",
    description="Market volatility and scalping opportunities",
    version="1.0.0"
)

class AgentInput(BaseModel):
    symbol: str
    timeframe: str
    data: Dict
    context: Optional[Dict] = None

class AgentOutput(BaseModel):
    agent_name: str = "marketsentinel"
    timestamp: datetime
    symbol: str
    confidence: float
    signal_type: Optional[str] = None
    reasoning: str
    data: Dict
    metadata: Optional[Dict] = None

# Agent-specific logic based on type

async def process_signal(input_data: AgentInput) -> AgentOutput:
    """Process market volatility analysis"""
    from .model import model
    from .utils import MarketsentinelUtils

    # Get market data
    market_data = input_data.data.get("market_data", {})
    volatility_data = input_data.data.get("volatility", {})

    # Run volatility analysis
    analysis = await model.predict({
        "market_data": market_data,
        "volatility": volatility_data,
        "symbol": input_data.symbol,
        "timeframe": input_data.timeframe
    })

    return AgentOutput(
        timestamp=datetime.now(),
        symbol=input_data.symbol,
        confidence=analysis.get("confidence", 0.0),
        reasoning=analysis.get("reasoning", "Market volatility analysis"),
        data=analysis,
        metadata={"agent_type": "volatility_analysis"}
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent": "marketsentinel", "timestamp": datetime.now()}

@app.post("/analyze", response_model=AgentOutput)
async def analyze(input_data: AgentInput):
    try:
        logger.info(f"Received analysis request for {input_data.symbol}")

        # Process the input data
        result = await process_signal(input_data)

        # Publish result to event bus (if available)
        await publish_result(result)

        return result

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def publish_result(result: AgentOutput):
    """Publish result to Redis event bus"""
    try:
        # This would connect to Redis in production
        logger.info(f"Publishing result for {result.symbol}")
    except Exception as e:
        logger.warning(f"Failed to publish result: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
