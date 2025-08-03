def risk_manager_node(state):
    state.reasoning["RiskManager"] = "Stub: Risk within acceptable range"
    state.next_agent = "MarketSentinel"
    return state
