from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# Dummy agent functions — replace with actual logic
def chart_analyst_node(state: dict) -> dict:
    print("?? Running chart analyst")
    return {**state, "chart_analysis": f"Chart analysis for {state['symbol']} on {state['timeframe']}"}

def macro_forecaster_node(state: dict) -> dict:
    print("?? Running macro forecaster")
    return {**state, "macro_outlook": f"Macro outlook for {state['symbol']}"}

def risk_manager_node(state: dict) -> dict:
    print("⚠️ Running risk manager")
    return {**state, "risk_score": f"Risk score for {state['symbol']}"}

def tactic_bot_node(state: dict) -> dict:
    print("?? Running tactic bot")
    decision = f"Execute BUY order on {state['symbol']}" if "EURUSD" in state["symbol"] else "HOLD"
    return {**state, "decision": decision}

# ✅ Main MCP function called by FastAPI
async def run_mcp_pipeline(symbol: str, timeframe: str) -> dict:
    initial_state = {"symbol": symbol, "timeframe": timeframe}

    # Build the graph
    builder = StateGraph(dict)

    # Add nodes
    builder.add_node("chart_analyst", RunnableLambda(chart_analyst_node))
    builder.add_node("macro_forecaster", RunnableLambda(macro_forecaster_node))
    builder.add_node("risk_manager", RunnableLambda(risk_manager_node))
    builder.add_node("tactic_bot", RunnableLambda(tactic_bot_node))

    # Set node execution order
    builder.set_entry_point("chart_analyst")
    builder.add_edge("chart_analyst", "macro_forecaster")
    builder.add_edge("macro_forecaster", "risk_manager")
    builder.add_edge("risk_manager", "tactic_bot")
    builder.set_finish_point("tactic_bot")

    # Compile and run
    graph = builder.compile()
    result = await graph.ainvoke(initial_state)
    return result
