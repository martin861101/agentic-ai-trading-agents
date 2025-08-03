import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class MarketsentinelUtils:
    """Utility functions for marketsentinel agent"""

    @staticmethod
    def validate_input(data: Dict) -> bool:
        """Validate input data format"""
        required_fields = ["symbol", "timeframe"]
        return all(field in data for field in required_fields)

    @staticmethod
    def calculate_confidence(factors: Dict) -> float:
        """Calculate confidence score based on multiple factors"""
        if not factors:
            return 0.0

        # Simple weighted average - customize per agent
        weights = {
            "strength": 0.4,
            "volume": 0.3,
            "trend": 0.2,
            "volatility": 0.1
        }

        score = 0.0
        total_weight = 0.0

        for factor, value in factors.items():
            if factor in weights:
                score += weights[factor] * value
                total_weight += weights[factor]

        return min(max(score / total_weight if total_weight > 0 else 0.0, 0.0), 1.0)

    @staticmethod
    def format_output(analysis: Dict) -> Dict:
        """Format analysis output for consistency"""
        return {
            "analysis": analysis,
            "timestamp": pd.Timestamp.now().isoformat(),
            "version": "1.0"
        }

# Agent-specific utility functions

def analyze_volatility(price_data: List[float], window: int = 20) -> Dict:
    """Analyze market volatility"""
    if len(price_data) < window:
        return {"volatility": 0, "regime": "unknown"}
    
    import numpy as np
    returns = np.diff(np.log(price_data))
    volatility = np.std(returns) * np.sqrt(252)  # Annualized
    
    # Classify volatility regime
    if volatility > 0.3:
        regime = "high"
    elif volatility > 0.15:
        regime = "medium"
    else:
        regime = "low"
    
    return {
        "volatility": round(volatility, 4),
        "regime": regime,
        "returns_std": np.std(returns),
        "avg_return": np.mean(returns)
    }

def detect_scalping_opportunities(tick_data: List[Dict]) -> List[Dict]:
    """Detect short-term scalping opportunities"""
    opportunities = []
    
    if len(tick_data) < 100:
        return opportunities
    
    # Simple momentum-based opportunities (placeholder)
    for i in range(10, len(tick_data) - 10):
        current_price = float(tick_data[i].get("price", 0))
        prev_prices = [float(tick_data[j].get("price", 0)) for j in range(i-10, i)]
        
        if current_price > max(prev_prices) * 1.001:  # 0.1% breakout
            opportunities.append({
                "type": "bullish_momentum",
                "price": current_price,
                "timestamp": tick_data[i].get("timestamp"),
                "strength": min((current_price / max(prev_prices) - 1) * 1000, 10)
            })
    
    return opportunities[:5]  # Return top 5

