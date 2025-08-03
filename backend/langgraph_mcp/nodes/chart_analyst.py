def chart_analyst_node(state):
    state.reasoning["ChartAnalyst"] = "Stub: Chart analysis complete"
    state.signal_type = "BUY"
    state.confidence = 0.85
    state.next_agent = "MacroForecaster"
    return state
