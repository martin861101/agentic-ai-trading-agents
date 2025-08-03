import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class ChartanalystUtils:
    """Utility functions for chartanalyst agent"""

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

def detect_patterns(candles: List[Dict]) -> Dict:
    """Detect chart patterns in candle data"""
    if len(candles) < 20:
        return {"pattern": "insufficient_data", "confidence": 0.0}
    
    # Placeholder pattern detection
    patterns = ["bullish_engulfing", "bearish_engulfing", "doji", "hammer", "shooting_star"]
    import random
    detected_pattern = random.choice(patterns)
    
    return {
        "pattern": detected_pattern,
        "confidence": random.uniform(0.3, 0.9),
        "support_levels": [random.uniform(100, 200) for _ in range(3)],
        "resistance_levels": [random.uniform(200, 300) for _ in range(3)]
    }

def calculate_indicators(candles: List[Dict]) -> Dict:
    """Calculate technical indicators"""
    if not candles:
        return {}
    
    # Simple moving averages (placeholder)
    closes = [float(c.get("close", 0)) for c in candles[-20:]]
    if len(closes) >= 10:
        sma_10 = sum(closes[-10:]) / 10
        sma_20 = sum(closes) / len(closes)
        return {"sma_10": sma_10, "sma_20": sma_20}
    
    return {}

