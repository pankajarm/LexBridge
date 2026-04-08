"""Semantic search agent: cross-lingual document retrieval using Harrier embeddings."""

from langdetect import detect

from src.agents.state import LexBridgeState

# Map query types to Harrier task prompts
TASK_MAP = {
    "document_search": "document_search",
    "risk_assessment": "risk_assessment",
    "entity_lookup": "entity_matching",
    "clause_comparison": "clause_comparison",
    "gap_analysis": "document_search",
}

# Supported languages for cross-lingual search
OTHER_LANG = {"en": "de", "de": "en"}


def semantic_search_node(state: LexBridgeState, embedder, vector_store) -> dict:
    """Retrieve relevant legal documents via cross-lingual semantic search.

    Uses a two-pass strategy to guarantee cross-lingual results:
    1. Search all documents (no language filter) for top results
    2. Search specifically in the OTHER language to surface cross-lingual hits
    3. Merge and deduplicate, ensuring both languages are represented
    """
    query = state["query"]
    query_type = state.get("query_type", "document_search")
    task = TASK_MAP.get(query_type, "document_search")

    # Embed query with task-specific Harrier prompt
    query_vector = embedder.embed_query(query, task=task)

    # Detect query language
    try:
        query_lang = detect(query)
        if query_lang not in OTHER_LANG:
            query_lang = "en"
    except Exception:
        query_lang = "en"

    cross_lang = OTHER_LANG.get(query_lang, "en")

    # Pass 1: Search all languages (top results naturally favor query language)
    all_results = vector_store.search(query_vector=query_vector, limit=10)

    # Pass 2: Search specifically in the OTHER language
    cross_results = vector_store.search(
        query_vector=query_vector, limit=5, language=cross_lang,
    )

    # Merge: deduplicate by doc_id, keeping higher score
    seen = {}
    for r in all_results + cross_results:
        doc_id = r.get("doc_id", r.get("title", ""))
        if doc_id not in seen or r.get("score", 0) > seen[doc_id].get("score", 0):
            seen[doc_id] = r

    # Sort by score descending
    merged = sorted(seen.values(), key=lambda x: x.get("score", 0), reverse=True)

    # Count languages
    lang_counts = {}
    for r in merged:
        lang = r.get("language", "?")
        lang_counts[lang] = lang_counts.get(lang, 0) + 1

    trace_entry = {
        "agent": "semantic_search",
        "action": "cross_lingual_search",
        "task": task,
        "query": query,
        "query_language": query_lang,
        "cross_language": cross_lang,
        "num_results": len(merged),
        "languages_found": lang_counts,
    }

    return {
        "search_results": merged,
        "agent_trace": state.get("agent_trace", []) + [trace_entry],
    }
