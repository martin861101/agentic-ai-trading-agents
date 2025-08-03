import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class PlatformpilotUtils:
    """Utility functions for platformpilot agent"""

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
# Agent-specific utilities go here
