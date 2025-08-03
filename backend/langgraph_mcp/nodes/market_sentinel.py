def market_sentinel_node(state):
    state.reasoning["MarketSentinel"] = "Stub: Market volatility low"
    state.next_agent = "TacticBot"
    return state
