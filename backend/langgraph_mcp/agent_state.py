from pydantic import BaseModel
from typing import Optional, Dict

class AgentState(BaseModel):
    symbol: str
    timeframe: str
    signal_type: Optional[str] = None
    confidence: Optional[float] = None
    reasoning: Dict[str, str] = {}
    raw_data: Dict[str, any] = {}
    next_agent: Optional[str] = None
