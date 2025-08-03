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
    title="Riskmanager Agent",
    description="Risk assessment and position sizing",
    version="1.0.0"
)

class AgentInput(BaseModel):
    symbol: str
    timeframe: str
    data: Dict
    context: Optional[Dict] = None

class AgentOutput(BaseModel):
    agent_name: str = "riskmanager"
    timestamp: datetime
    symbol: str
    confidence: float
    signal_type: Optional[str] = None
    reasoning: str
    data: Dict
    metadata: Optional[Dict] = None

# Agent-specific logic based on type

async def process_signal(input_data: AgentInput) -> AgentOutput:
    """Process risk management analysis"""
    from .model import model
    from .utils import RiskmanagerUtils

    # Get portfolio info and signal details
    portfolio = input_data.data.get("portfolio", {})
    signal_data = input_data.data.get("signal", {})

    # Run risk analysis
    analysis = await model.predict({
        "portfolio": portfolio,
        "signal": signal_data,
        "symbol": input_data.symbol
    })

    return AgentOutput(
        timestamp=datetime.now(),
        symbol=input_data.symbol,
        confidence=analysis.get("confidence", 0.0),
        reasoning=analysis.get("reasoning", "Risk assessment analysis"),
        data=analysis,
        metadata={"agent_type": "risk_management"}
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent": "riskmanager", "timestamp": datetime.now()}

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
    uvicorn.run(app, host="0.0.0.0", port=8002)
