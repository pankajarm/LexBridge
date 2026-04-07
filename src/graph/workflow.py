"""LangGraph StateGraph workflow for LexBridge multi-agent system."""

from functools import partial

from langgraph.graph import END, StateGraph

from src.agents.state import LexBridgeState
from src.agents.supervisor import supervisor_node
from src.agents.semantic_search_agent import semantic_search_node
from src.agents.graph_query_agent import graph_query_node
from src.agents.risk_analysis_agent import risk_analysis_node


SYSTEM_PROMPT = (
    "You are LexBridge, a cross-lingual M&A due diligence intelligence system. "
    "You analyze legal documents across languages and jurisdictions, "
    "assess litigation risks, compare contract clauses, and identify due diligence gaps. "
    "Provide clear, well-structured analysis with citations to source documents."
)


def synthesizer_node(state: LexBridgeState, llm) -> dict:
    """Build final response from all agent outputs."""
    search_results = state.get("search_results", [])
    graph_results = state.get("graph_results", [])
    risk_report = state.get("risk_report", {})

    # Build context from all sources
    context_parts = []

    if search_results:
        context_parts.append("## Document Search Results")
        for i, doc in enumerate(search_results[:8], 1):
            lang_flag = {"en": "US", "de": "DE"}.get(doc.get("language", ""), "??")
            context_parts.append(
                f"{i}. [{lang_flag}] {doc.get('title', 'Untitled')} "
                f"(score: {doc.get('score', 0):.3f}, type: {doc.get('doc_type', 'unknown')})\n"
                f"   {doc.get('summary', '')[:300]}"
            )

    if graph_results:
        context_parts.append("\n## Knowledge Graph Results")
        for item in graph_results[:10]:
            if isinstance(item, dict):
                context_parts.append(f"- {item}")

    if risk_report:
        context_parts.append(f"\n## Risk Analysis Report\n{risk_report}")

    context = "\n".join(context_parts)
    query = state.get("query", "")

    prompt = (
        f"User query: {query}\n\n"
        f"Available intelligence:\n{context}\n\n"
        f"Provide a comprehensive answer based on the above data. "
        f"Cite specific documents and data points. "
        f"If results span multiple languages, note the cross-lingual findings."
    )

    response = llm.generate(prompt, system_prompt=SYSTEM_PROMPT)

    trace_entry = {
        "agent": "synthesizer",
        "action": "generate_response",
        "context_sources": {
            "search_results": len(search_results),
            "graph_results": len(graph_results),
            "has_risk_report": bool(risk_report),
        },
    }

    return {
        "final_response": response,
        "agent_trace": state.get("agent_trace", []) + [trace_entry],
    }


def _route_after_supervisor(state: LexBridgeState) -> str:
    """Route from supervisor to first processing agent."""
    query_type = state.get("query_type", "document_search")
    if query_type == "entity_lookup":
        return "graph_query"
    # document_search, risk_assessment, clause_comparison, gap_analysis -> semantic_search
    return "semantic_search"


def _route_after_search(state: LexBridgeState) -> str:
    """Route from semantic search to next agent."""
    query_type = state.get("query_type", "document_search")
    if query_type in ("risk_assessment", "gap_analysis"):
        return "graph_query"
    if query_type == "clause_comparison":
        return "risk_analysis"
    return "synthesizer"


def _route_after_graph(state: LexBridgeState) -> str:
    """Route from graph query to next agent."""
    query_type = state.get("query_type", "document_search")
    if query_type in ("risk_assessment", "gap_analysis"):
        return "risk_analysis"
    return "synthesizer"


def build_workflow(embedder, vector_store, graph_store, llm) -> StateGraph:
    """Build and compile the LexBridge LangGraph workflow."""
    workflow = StateGraph(LexBridgeState)

    # Add nodes with dependencies injected via partial
    workflow.add_node("supervisor", partial(supervisor_node, llm=llm))
    workflow.add_node("semantic_search", partial(semantic_search_node, embedder=embedder, vector_store=vector_store))
    workflow.add_node("graph_query", partial(graph_query_node, graph_store=graph_store, llm=llm))
    workflow.add_node("risk_analysis", partial(risk_analysis_node, embedder=embedder, llm=llm))
    workflow.add_node("synthesizer", partial(synthesizer_node, llm=llm))

    # Set entry point
    workflow.set_entry_point("supervisor")

    # Conditional routing from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        _route_after_supervisor,
        {"semantic_search": "semantic_search", "graph_query": "graph_query"},
    )

    # Conditional routing from semantic search
    workflow.add_conditional_edges(
        "semantic_search",
        _route_after_search,
        {"graph_query": "graph_query", "risk_analysis": "risk_analysis", "synthesizer": "synthesizer"},
    )

    # Conditional routing from graph query
    workflow.add_conditional_edges(
        "graph_query",
        _route_after_graph,
        {"risk_analysis": "risk_analysis", "synthesizer": "synthesizer"},
    )

    # Risk analysis always goes to synthesizer
    workflow.add_edge("risk_analysis", "synthesizer")

    # Synthesizer always ends
    workflow.add_edge("synthesizer", END)

    return workflow.compile()
