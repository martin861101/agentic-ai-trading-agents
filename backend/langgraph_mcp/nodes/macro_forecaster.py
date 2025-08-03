def macro_forecaster_node(state):
    state.reasoning["MacroForecaster"] = "Stub: Macro forecast positive"
    state.next_agent = "RiskManager"
    return state
