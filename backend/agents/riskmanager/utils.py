import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class RiskmanagerUtils:
    """Utility functions for riskmanager agent"""

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

def calculate_position_size(portfolio_value: float, risk_percent: float, stop_loss_distance: float) -> Dict:
    """Calculate optimal position size based on risk management"""
    if stop_loss_distance <= 0 or portfolio_value <= 0:
        return {"position_size": 0, "reason": "invalid_parameters"}
    
    risk_amount = portfolio_value * (risk_percent / 100)
    position_size = risk_amount / stop_loss_distance
    
    return {
        "position_size": round(position_size, 2),
        "risk_amount": risk_amount,
        "risk_percent": risk_percent,
        "stop_loss_distance": stop_loss_distance
    }

def assess_risk_reward(entry_price: float, stop_loss: float, take_profit: float) -> Dict:
    """Assess risk-reward ratio"""
    if entry_price <= 0:
        return {"risk_reward": 0, "assessment": "invalid"}
    
    risk = abs(entry_price - stop_loss)
    reward = abs(take_profit - entry_price)
    
    if risk <= 0:
        return {"risk_reward": float('inf'), "assessment": "no_risk"}
    
    ratio = reward / risk
    
    return {
        "risk_reward": round(ratio, 2),
        "risk": risk,
        "reward": reward,
        "assessment": "good" if ratio >= 2.0 else "acceptable" if ratio >= 1.5 else "poor"
    }

