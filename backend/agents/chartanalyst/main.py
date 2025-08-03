# backend/agents/chartanalyst/main.py
from prompts import generate_signal_prompt
from .mistral_client import query_mistral
from .tavily_client import get_web_insights

def chart_analyst_node(data: dict) -> dict:
    symbol = data.get("symbol", "EURUSD")
    timeframe = data.get("timeframe", "1h")

    print(f"[chart_analyst] Analyzing {symbol} on {timeframe}...")

    insights = get_web_insights(f"{symbol} forex news")
    prompt = generate_signal_prompt(symbol=symbol, timeframe=timeframe, web_insights=insights)
    response = query_mistral(prompt)

    return {
        "agent": "chart_analyst",
        "symbol": symbol,
        "timeframe": timeframe,
        "signal": response
    }
