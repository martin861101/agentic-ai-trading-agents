def tacticbot_node(state):
    state.reasoning["TacticBot"] = "Stub: Executing BUY"
    state.next_agent = "PlatformPilot"
    return state
