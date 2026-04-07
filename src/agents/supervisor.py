"""Supervisor agent: classifies intent and routes to specialist agents."""

from src.agents.state import LexBridgeState


def supervisor_node(state: LexBridgeState, llm) -> dict:
    """Classify user query and set routing metadata."""
    query = state["query"]
    query_type = llm.classify_intent(query)

    trace_entry = {
        "agent": "supervisor",
        "action": "classify_intent",
        "query": query,
        "classified_as": query_type,
    }

    return {
        "query_type": query_type,
        "agent_trace": state.get("agent_trace", []) + [trace_entry],
    }
