"""LangGraph shared state for LexBridge multi-agent system."""

from typing import Annotated, Literal

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class LexBridgeState(TypedDict):
    """Shared state across all agents in the LexBridge workflow."""
    messages: Annotated[list, add_messages]
    query: str
    query_type: Literal[
        "document_search",
        "risk_assessment",
        "entity_lookup",
        "clause_comparison",
        "gap_analysis",
    ]
    search_results: list[dict]
    graph_results: list[dict]
    risk_report: dict
    agent_trace: list[dict]
    final_response: str
