# backend/agents/chartanalyst/prompts.py

def generate_signal_prompt(symbol: str, timeframe: str, web_insights: str = "", chart_notes: str = "") -> str:
    return f"""
Analyze the trading opportunity for {symbol} on the {timeframe} timeframe.
Consider:
- Technical analysis signals
- Current news sentiment or relevant insights
- Chart notes: {chart_notes}
- Web insights: {web_insights}

Provide:
1. Signal Type (BUY/SELL/HOLD)
2. Confidence score (0-1)
3. Reasoning (max 50 words)
"""
