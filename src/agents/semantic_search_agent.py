"""Semantic search agent: cross-lingual document retrieval using Harrier embeddings."""

from src.agents.state import LexBridgeState

# Map query types to Harrier task prompts
TASK_MAP = {
    "document_search": "document_search",
    "risk_assessment": "risk_assessment",
    "entity_lookup": "entity_matching",
    "clause_comparison": "clause_comparison",
    "gap_analysis": "document_search",
}


def semantic_search_node(state: LexBridgeState, embedder, vector_store) -> dict:
    """Retrieve relevant legal documents via cross-lingual semantic search."""
    query = state["query"]
    query_type = state.get("query_type", "document_search")
    task = TASK_MAP.get(query_type, "document_search")

    # Embed query with task-specific Harrier prompt
    query_vector = embedder.embed_query(query, task=task)

    # Apply filters based on query type
    kwargs = {"limit": 10}
    if query_type == "clause_comparison":
        kwargs["doc_type"] = "settlement_agreement"
        kwargs["limit"] = 15
    elif query_type == "risk_assessment":
        kwargs["limit"] = 15

    # Search across all languages (Harrier handles cross-lingual natively)
    results = vector_store.search(query_vector=query_vector, **kwargs)

    trace_entry = {
        "agent": "semantic_search",
        "action": "cross_lingual_search",
        "task": task,
        "query": query,
        "num_results": len(results),
        "languages_found": list({r.get("language", "unknown") for r in results}),
    }

    return {
        "search_results": results,
        "agent_trace": state.get("agent_trace", []) + [trace_entry],
    }
